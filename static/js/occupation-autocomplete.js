/** ESCO occupation autocomplete + material duties population prompt. */
(function () {
  const input = document.getElementById("occupation");
  const listbox = document.getElementById("occupation-suggestions");
  const status = document.getElementById("occupation-status");
  const dutiesField = document.querySelector('textarea[name="material_duties"]');
  const meansBox = document.getElementById("material-duties-means");
  const meansLead = document.getElementById("material-duties-means-lead");
  const meansParagraph = document.getElementById("material-duties-means-paragraph");
  const meansOptional = document.getElementById("material-duties-means-optional");
  const plainChecklist = document.getElementById("occupation-plain-checklist");
  const roleRequirementsText = document.getElementById("occupation-role-requirements-text");
  const roleConfirmBtn = document.getElementById("occupation-role-confirm");
  const roleRejectBtn = document.getElementById("occupation-role-reject");
  const roleManualWrap = document.getElementById("occupation-role-manual");
  const roleManualInput = document.getElementById("occupation-role-manual-input");
  const profileSaveBtn = document.getElementById("occupation-profile-save");
  const autosaveStatus = document.getElementById("occupation-autosave-status");
  const profileUpdatedBox = document.getElementById("occupation-profile-updated");
  const updatedLead = document.getElementById("occupation-updated-lead");
  const updatedList = document.getElementById("occupation-updated-list");
  const updatedRole = document.getElementById("occupation-updated-role");
  const profileHidden = document.getElementById("occupation_profile_json");
  const intakeForm = document.querySelector(".intake-wizard-form");
  const claimId = intakeForm?.dataset.claimId ? Number(intakeForm.dataset.claimId) : null;
  const functionalBox = document.getElementById("functional-duty-map");
  const functionalPlaceholder = document.getElementById("functional-map-placeholder");
  const functionalIntro = document.getElementById("functional-map-intro");
  const functionalGrid = document.getElementById("functional-map-grid");
  const gotoOccupationBtn = document.getElementById("goto-occupation-for-map");

  const dutiesModal = document.getElementById("duties-prompt-modal");
  const dutiesBackdrop = document.getElementById("duties-prompt-backdrop");
  const dutiesTitle = document.getElementById("duties-prompt-title");
  const dutiesSummary = document.getElementById("duties-prompt-summary");
  const dutiesYes = document.getElementById("duties-prompt-yes");
  const dutiesAppend = document.getElementById("duties-prompt-append");
  const dutiesNo = document.getElementById("duties-prompt-no");
  const dutiesClose = document.getElementById("duties-prompt-close");

  if (!input || !listbox) return;

  let symptomTips = {};
  const configEl = document.getElementById("illness-story-config");
  if (configEl) {
    try {
      const cfg = JSON.parse(configEl.textContent || "{}");
      symptomTips = cfg.symptom_definitions || {};
    } catch (e) {
      symptomTips = {};
    }
  }

  function lookupSymptomTip(text) {
    const t = (text || "").trim();
    if (!t) return "";
    if (symptomTips[t]) return symptomTips[t];
    const lower = t.toLowerCase();
    const exact = Object.keys(symptomTips).find((k) => k.toLowerCase() === lower);
    if (exact) return symptomTips[exact];
    return "Illness link for this functional area — carries into your health story bridge.";
  }

  function attachTermTip(el, text) {
    if (!el || !window.ClaimBuddyTermTips) return;
    const tip = lookupSymptomTip(text);
    if (tip) window.ClaimBuddyTermTips.attach(el, tip);
  }

  let debounceTimer = null;
  let activeIndex = -1;
  let suggestions = [];
  let pendingProfile = null;
  let activeProfile = null;
  let plainItems = [];
  let roleRequirementsState = "confirmed";
  let lastSelectedTitle = "";

  function setStatus(text, loading) {
    if (!status) return;
    status.textContent = text || "";
    status.classList.toggle("is-loading", !!loading);
  }

  function closeListbox() {
    listbox.hidden = true;
    input.setAttribute("aria-expanded", "false");
    activeIndex = -1;
    listbox.innerHTML = "";
    suggestions = [];
  }

  function openListbox() {
    listbox.hidden = false;
    input.setAttribute("aria-expanded", "true");
  }

  function renderSuggestions(items) {
    suggestions = items;
    listbox.innerHTML = "";
    activeIndex = -1;
    if (!items.length) {
      const li = document.createElement("li");
      li.className = "occ-suggestion-empty";
      li.textContent = "No matches — keep typing or enter your own title.";
      listbox.appendChild(li);
      openListbox();
      return;
    }
    items.forEach((item, index) => {
      const li = document.createElement("li");
      li.id = "occ-option-" + index;
      li.setAttribute("role", "option");
      li.dataset.index = String(index);
      li.innerHTML =
        "<strong>" +
        escapeHtml(item.title) +
        "</strong>" +
        (item.code ? '<span class="occ-code">ESCO ' + escapeHtml(item.code) + "</span>" : "") +
        (item.hint && item.hint !== item.title
          ? '<span class="occ-hint">' + escapeHtml(item.hint) + "</span>"
          : "");
      li.addEventListener("mousedown", (e) => {
        e.preventDefault();
        selectSuggestion(index);
      });
      listbox.appendChild(li);
    });
    openListbox();
  }

  function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }

  function highlightOption(index) {
    const options = listbox.querySelectorAll('[role="option"]');
    options.forEach((el, i) => {
      el.classList.toggle("is-active", i === index);
    });
    activeIndex = index;
    if (options[index]) {
      input.setAttribute("aria-activedescendant", options[index].id);
    }
  }

  async function search(query) {
    if (query.trim().length < 2) {
      closeListbox();
      setStatus("");
      return;
    }
    setStatus("Searching ESCO occupation database…", true);
    try {
      const res = await fetch(
        "/api/occupations/search?q=" + encodeURIComponent(query.trim())
      );
      const data = await res.json();
      renderSuggestions(data.results || []);
      setStatus(
        (data.results || []).length
          ? "Select a standard occupation or keep your own wording."
          : "No ESCO match — free text is fine."
      );
    } catch (_err) {
      setStatus("Occupation search unavailable — enter title manually.");
      closeListbox();
    }
  }

  function openDutiesPrompt(profile) {
    pendingProfile = profile;
    if (dutiesTitle) dutiesTitle.textContent = profile.title;
    if (dutiesSummary) {
      dutiesSummary.textContent =
        "We can draft material duties from the ESCO profile (" +
        profile.essential_count +
        " essential skills" +
        (profile.optional_count ? ", " + profile.optional_count + " optional" : "") +
        "). You should edit to match your actual role.";
    }
    const hasExisting = dutiesField && dutiesField.value.trim().length > 0;
    if (dutiesAppend) dutiesAppend.hidden = !hasExisting;
    if (dutiesYes) dutiesYes.textContent = hasExisting ? "Replace duties" : "Yes, populate duties";
    dutiesModal.hidden = false;
    dutiesBackdrop.hidden = false;
    document.body.classList.add("modal-open");
  }

  function closeDutiesPrompt() {
    dutiesModal.hidden = true;
    dutiesBackdrop.hidden = true;
    document.body.classList.remove("modal-open");
    pendingProfile = null;
  }

  function dispatchFunctionalSelection(domainId, illnessLink, symptom) {
    document.dispatchEvent(
      new CustomEvent("claimbuddy:functional-domain-selected", {
        detail: {
          domainId,
          illnessLink,
          symptom: (symptom || "").trim(),
          fromMap: true,
        },
      })
    );
  }

  function hideFunctionalMap() {
    if (functionalBox) functionalBox.hidden = true;
    if (functionalGrid) functionalGrid.innerHTML = "";
    if (functionalIntro) functionalIntro.textContent = "";
    if (functionalPlaceholder) functionalPlaceholder.hidden = false;
  }

  function showFunctionalMap(profile) {
    const fmap = profile.functional_map;
    if (!functionalBox || !fmap || !functionalGrid) {
      hideFunctionalMap();
      return;
    }
    if (functionalIntro) functionalIntro.textContent = fmap.intro || "";
    functionalGrid.innerHTML = "";
    (fmap.domains || []).forEach((domain) => {
      const card = document.createElement("article");
      card.className =
        "functional-map-card is-clickable" + (domain.active ? " is-active" : " is-muted");
      card.dataset.domain = domain.id;
      card.dataset.illnessLink = domain.illness_link || "";
      const head = document.createElement("header");
      head.className = "functional-map-card-head";
      head.innerHTML =
        "<span class='functional-map-icon'>" +
        (domain.icon || "") +
        "</span><strong>" +
        escapeHtml(domain.label) +
        "</strong>";
      card.appendChild(head);

      const hint = document.createElement("p");
      hint.className = "functional-map-hint";
      hint.textContent = domain.hint || "";
      card.appendChild(hint);
      if (domain.hint) {
        attachTermTip(card, domain.hint);
      } else {
        attachTermTip(
          card,
          "Functional area — click to use in your symptom-to-duty health story bridge."
        );
      }

      if (domain.items && domain.items.length) {
        const ul = document.createElement("ul");
        domain.items.forEach((item) => {
          const li = document.createElement("li");
          li.textContent = item;
          ul.appendChild(li);
        });
        card.appendChild(ul);
      } else {
        const empty = document.createElement("p");
        empty.className = "functional-map-empty";
        empty.textContent = "Not flagged from this profile — confirm if it applies to your role.";
        card.appendChild(empty);
      }

      const linkWrap = document.createElement("div");
      linkWrap.className = "functional-map-illness";
      const linkLabel = document.createElement("span");
      linkLabel.className = "functional-map-illness-label";
      linkLabel.textContent = "Illness link →";
      linkWrap.appendChild(linkLabel);
      const chipRow = document.createElement("div");
      chipRow.className = "functional-map-illness-chips";
      const tokens = (domain.illness_link || "")
        .split(/[,;]+/)
        .map((s) => s.trim())
        .filter((s) => s.length >= 3);
      if (tokens.length) {
        tokens.forEach((token) => {
          const chip = document.createElement("button");
          chip.type = "button";
          chip.className = "functional-map-illness-chip";
          chip.textContent = token;
          attachTermTip(chip, token);
          chip.addEventListener("click", (e) => {
            e.stopPropagation();
            dispatchFunctionalSelection(domain.id, domain.illness_link || "", token);
          });
          chipRow.appendChild(chip);
        });
      } else {
        const fallback = document.createElement("span");
        fallback.className = "functional-map-illness-empty";
        fallback.textContent = "Add symptoms in story builder";
        chipRow.appendChild(fallback);
      }
      linkWrap.appendChild(chipRow);
      card.appendChild(linkWrap);

      card.addEventListener("click", () => {
        dispatchFunctionalSelection(domain.id, domain.illness_link || "", "");
      });

      functionalGrid.appendChild(card);
    });
    functionalBox.hidden = false;
    if (functionalPlaceholder) functionalPlaceholder.hidden = true;
    document.dispatchEvent(
      new CustomEvent("claimbuddy:functional-map-ready", { detail: { profile } })
    );
    setStatus(
      "Functional map ready on Health story (step 5) — use it in the functional-capacity builder."
    );
  }

  function hideMeansBox() {
    if (meansBox) meansBox.hidden = true;
    if (plainChecklist) plainChecklist.innerHTML = "";
    if (meansLead) meansLead.textContent = "";
    if (meansParagraph) {
      meansParagraph.textContent = "";
      meansParagraph.hidden = true;
    }
    if (meansOptional) {
      meansOptional.textContent = "";
      meansOptional.hidden = true;
    }
    if (profileUpdatedBox) profileUpdatedBox.hidden = true;
    if (autosaveStatus) autosaveStatus.textContent = "";
    activeProfile = null;
    plainItems = [];
    hideFunctionalMap();
  }

  function roleRequirementsFlat(data) {
    if (!data) return "";
    if (typeof data === "string") return data;
    return data.text || "";
  }

  function renderRoleRequirements(data) {
    if (!roleRequirementsText) return;
    roleRequirementsText.innerHTML = "";
    if (!data) return;

    if (typeof data === "string") {
      const legacy = document.createElement("p");
      legacy.className = "occupation-role-legacy-text";
      legacy.textContent = data;
      roleRequirementsText.appendChild(legacy);
      return;
    }

    const structured = document.createElement("div");
    structured.className = "occupation-role-structured";

    const headline = document.createElement("p");
    headline.className = "occupation-role-headline";
    headline.innerHTML =
      "<span class='occupation-role-title'>" +
      escapeHtml(data.title || "This role") +
      "</span>" +
      (data.intro ? "<span class='occupation-role-headline-sub'>" + escapeHtml(data.intro) + "</span>" : "");
    structured.appendChild(headline);

    const grid = document.createElement("div");
    grid.className = "occupation-role-grid";
    (data.categories || []).forEach((cat) => {
      const card = document.createElement("article");
      card.className = "occupation-role-card occupation-role-card--" + (cat.id || "core");

      const head = document.createElement("header");
      head.className = "occupation-role-card-head";
      head.innerHTML =
        "<span class='occupation-role-card-icon' aria-hidden='true'>" +
        (cat.icon || "📋") +
        "</span><div><strong>" +
        escapeHtml(cat.label || "Demands") +
        "</strong>" +
        (cat.hint ? "<span class='occupation-role-card-hint'>" + escapeHtml(cat.hint) + "</span>" : "") +
        "</div>";
      card.appendChild(head);

      const items = cat.items || [];
      if (items.length) {
        const ul = document.createElement("ul");
        ul.className = "occupation-role-card-list";
        items.forEach((item) => {
          const li = document.createElement("li");
          li.textContent = item;
          ul.appendChild(li);
        });
        card.appendChild(ul);
      }
      grid.appendChild(card);
    });
    structured.appendChild(grid);

    if (data.fallback) {
      const fallback = document.createElement("p");
      fallback.className = "occupation-role-fallback";
      fallback.textContent = data.fallback;
      structured.appendChild(fallback);
    }

    if (data.footer) {
      const foot = document.createElement("aside");
      foot.className = "occupation-role-footer";
      foot.innerHTML = "<strong>Confirm fit</strong> — " + escapeHtml(data.footer);
      structured.appendChild(foot);
    }

    roleRequirementsText.appendChild(structured);
  }

  function setRoleRequirementsState(state) {
    roleRequirementsState = state;
    roleConfirmBtn?.classList.toggle("is-selected", state === "confirmed");
    roleRejectBtn?.classList.toggle("is-selected", state === "rejected");
    if (roleManualWrap) roleManualWrap.hidden = state !== "rejected";
  }

  function initPlainItems(bullets) {
    plainItems = (bullets || []).map((text) => ({
      text,
      status: "confirmed",
      replacement: "",
    }));
  }

  function renderPlainChecklist() {
    if (!plainChecklist) return;
    plainChecklist.innerHTML = "";
    if (!plainItems.length) {
      const empty = document.createElement("li");
      empty.className = "occupation-plain-empty";
      empty.textContent = "No plain-term bullets — add duties manually above.";
      plainChecklist.appendChild(empty);
      return;
    }
    plainItems.forEach((item, index) => {
      const li = document.createElement("li");
      li.className = "occupation-plain-item" + (item.status === "rejected" ? " is-rejected" : "");
      li.dataset.index = String(index);

      const row = document.createElement("div");
      row.className = "occupation-plain-row";

      const text = document.createElement("span");
      text.className = "occupation-plain-text";
      text.textContent = item.text;

      const actions = document.createElement("div");
      actions.className = "occupation-plain-actions";
      actions.setAttribute("role", "group");
      actions.setAttribute("aria-label", "Confirm or reject this plain term");

      const tick = document.createElement("button");
      tick.type = "button";
      tick.className = "occupation-plain-btn occupation-plain-tick" + (item.status !== "rejected" ? " is-selected" : "");
      tick.title = "This is right for my role";
      tick.textContent = "✓";
      tick.addEventListener("click", () => {
        item.status = "confirmed";
        item.replacement = "";
        renderPlainChecklist();
      });

      const cross = document.createElement("button");
      cross.type = "button";
      cross.className = "occupation-plain-btn occupation-plain-cross" + (item.status === "rejected" ? " is-selected" : "");
      cross.title = "Not right — I'll correct it";
      cross.textContent = "✗";
      cross.addEventListener("click", () => {
        item.status = "rejected";
        renderPlainChecklist();
        const manual = plainChecklist.querySelector(
          '.occupation-plain-item[data-index="' + index + '"] .occupation-plain-manual-input'
        );
        manual?.focus();
      });

      actions.appendChild(tick);
      actions.appendChild(cross);
      row.appendChild(text);
      row.appendChild(actions);
      li.appendChild(row);

      if (item.status === "rejected") {
        const manualWrap = document.createElement("div");
        manualWrap.className = "occupation-plain-manual";
        const label = document.createElement("label");
        label.textContent = "What it should say for your role";
        const input = document.createElement("input");
        input.type = "text";
        input.className = "occupation-plain-manual-input";
        input.placeholder = "e.g. you lead client workshops, not site inspections";
        input.value = item.replacement || "";
        input.addEventListener("input", () => {
          item.replacement = input.value;
        });
        manualWrap.appendChild(label);
        manualWrap.appendChild(input);
        li.appendChild(manualWrap);
      }

      plainChecklist.appendChild(li);
    });
  }

  function resolvedPlainText(item) {
    if (item.status === "rejected" && item.replacement.trim()) {
      return item.replacement.trim();
    }
    if (item.status === "rejected") {
      return null;
    }
    return item.text;
  }

  function buildConfirmedProfile() {
    if (!activeProfile) return null;
    const plain = activeProfile.plain_summary || {};
    const confirmedBullets = plainItems
      .map((item) => {
        const text = resolvedPlainText(item);
        return text
          ? {
              original: item.text,
              text,
              status: item.status,
              replacement: item.replacement || "",
            }
          : null;
      })
      .filter(Boolean);

    const roleText =
      roleRequirementsState === "rejected" && roleManualInput?.value.trim()
        ? roleManualInput.value.trim()
        : roleRequirementsFlat(plain.role_requirements);

    const lines = [];
    lines.push("Confirmed occupation profile: " + (activeProfile.title || input?.value || "Role"));
    lines.push("");
    if (confirmedBullets.length) {
      lines.push("Plain terms (confirmed):");
      confirmedBullets.forEach((b) => lines.push("• " + b.text));
      lines.push("");
    }
    if (roleText) {
      lines.push("Role requirements (confirmed):");
      lines.push(roleText);
    }

    return {
      esco_uri: activeProfile.uri || "",
      title: activeProfile.title || "",
      saved_at: new Date().toISOString(),
      plain_terms: plainItems.map((item) => ({
        text: item.text,
        status: item.status,
        replacement: item.replacement || "",
        resolved: resolvedPlainText(item),
      })),
      role_requirements: {
        suggested: plain.role_requirements || null,
        status: roleRequirementsState,
        manual: roleManualInput?.value.trim() || "",
        resolved: roleText,
      },
      updated_summary: {
        lead: plain.lead || "",
        bullets: confirmedBullets.map((b) => b.text),
      },
      material_duties_text: lines.join("\n").trim(),
    };
  }

  function showUpdatedBox(profile) {
    if (!profileUpdatedBox) return;
    const summary = profile.updated_summary || {};
    if (updatedLead) {
      updatedLead.textContent =
        summary.lead || "Your confirmed plain terms for " + (profile.title || "this role") + ":";
    }
    if (updatedList) {
      updatedList.innerHTML = "";
      (summary.bullets || []).forEach((text) => {
        const li = document.createElement("li");
        li.textContent = text;
        updatedList.appendChild(li);
      });
      updatedList.hidden = !(summary.bullets || []).length;
    }
    if (updatedRole) {
      const rr = profile.role_requirements || {};
      updatedRole.textContent = rr.resolved ? "Role requirements: " + rr.resolved : "";
      updatedRole.hidden = !rr.resolved;
    }
    profileUpdatedBox.hidden = false;
    profileUpdatedBox.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  function persistProfileHidden(profile) {
    if (profileHidden) {
      profileHidden.value = JSON.stringify(profile);
      profileHidden.dispatchEvent(new Event("change", { bubbles: true }));
    }
  }

  async function saveOccupationProfile() {
    const profile = buildConfirmedProfile();
    if (!profile) return;

    const rejectedMissing = plainItems.some(
      (item) => item.status === "rejected" && !item.replacement.trim()
    );
    if (rejectedMissing) {
      if (autosaveStatus) {
        autosaveStatus.textContent = "Please fill in manual text for every crossed-out item.";
      }
      return;
    }
    if (roleRequirementsState === "rejected" && !roleManualInput?.value.trim()) {
      if (autosaveStatus) {
        autosaveStatus.textContent = "Please describe what your role actually requires.";
      }
      roleManualInput?.focus();
      return;
    }

    if (dutiesField) {
      dutiesField.value = profile.material_duties_text;
      dutiesField.dispatchEvent(new Event("input", { bubbles: true }));
    }
    persistProfileHidden(profile);
    showUpdatedBox(profile);

    if (autosaveStatus) autosaveStatus.textContent = "Saving…";

    if (claimId) {
      try {
        const res = await fetch("/api/claim/" + claimId + "/occupation-profile", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            occupation: activeProfile?.title || input?.value || "",
            material_duties: profile.material_duties_text,
            profile,
          }),
        });
        if (!res.ok) throw new Error("save failed");
        const data = await res.json();
        if (autosaveStatus) {
          autosaveStatus.textContent = "Saved " + (data.updated_at ? new Date(data.updated_at).toLocaleString() : "to claim");
        }
        setStatus("Occupation profile confirmed and saved.");
      } catch (_err) {
        if (autosaveStatus) {
          autosaveStatus.textContent = "Saved locally — full save when you submit the form.";
        }
      }
    } else if (autosaveStatus) {
      autosaveStatus.textContent = "Saved to form — will persist when you create the workspace.";
    }
  }

  function showMeansBox(profile) {
    const plain = profile.plain_summary;
    if (!meansBox || !plain) {
      hideMeansBox();
      return;
    }
    activeProfile = profile;
    initPlainItems(plain.bullets || []);
    setRoleRequirementsState("confirmed");
    if (roleManualInput) roleManualInput.value = "";
    if (profileUpdatedBox) profileUpdatedBox.hidden = true;
    if (autosaveStatus) autosaveStatus.textContent = "";

    if (meansLead) meansLead.textContent = plain.lead || "";
    if (meansParagraph) {
      meansParagraph.textContent = plain.paragraph || "";
      meansParagraph.hidden = !plain.paragraph;
    }
    renderRoleRequirements(plain.role_requirements);
    renderPlainChecklist();

    if (meansOptional) {
      const extras = plain.optional_bullets || [];
      if (extras.length) {
        meansOptional.textContent =
          "You may also: " +
          extras.map((e) => e.replace(/^you /i, "")).join("; ") +
          ".";
        meansOptional.hidden = false;
      } else {
        meansOptional.hidden = true;
      }
    }
    meansBox.hidden = false;
    meansBox.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  function restoreSavedProfile() {
    if (!profileHidden?.value.trim()) return;
    try {
      const saved = JSON.parse(profileHidden.value);
      if (!saved || !saved.title) return;
      if (updatedLead && saved.updated_summary) {
        showUpdatedBox(saved);
      }
      if (meansBox && saved.plain_terms?.length) {
        activeProfile = {
          title: saved.title,
          uri: saved.esco_uri || "",
          plain_summary: {
            lead: saved.updated_summary?.lead || "",
            bullets: saved.plain_terms.map((t) => t.text),
            role_requirements: saved.role_requirements?.suggested || "",
          },
        };
        plainItems = saved.plain_terms.map((t) => ({
          text: t.text,
          status: t.status || "confirmed",
          replacement: t.replacement || "",
        }));
        setRoleRequirementsState(saved.role_requirements?.status || "confirmed");
        if (roleManualInput) {
          roleManualInput.value = saved.role_requirements?.manual || "";
        }
        if (meansLead) meansLead.textContent = activeProfile.plain_summary.lead;
        renderRoleRequirements(activeProfile.plain_summary.role_requirements);
        renderPlainChecklist();
        meansBox.hidden = false;
      }
    } catch (_e) {
      /* ignore invalid json */
    }
  }

  function applyDuties(mode) {
    if (!pendingProfile) return;
    const profile = pendingProfile;
    if (mode === "append" && dutiesField?.value.trim() && profile.duties_text) {
      profile.duties_text =
        dutiesField.value.trim() + "\n\n---\n\n" + profile.duties_text;
    }
    activeProfile = profile;
    showMeansBox(profile);
    showFunctionalMap(profile);
    closeDutiesPrompt();
    setStatus("Tick plain terms, confirm role requirements, then Save confirmed profile.");
  }

  async function selectSuggestion(index) {
    const item = suggestions[index];
    if (!item) return;
    lastSelectedTitle = item.title;
    input.value = item.title;
    closeListbox();
    setStatus("Loading duties profile for " + item.title + "…", true);
    try {
      const res = await fetch(
        "/api/occupations/duties?uri=" + encodeURIComponent(item.uri)
      );
      if (!res.ok) throw new Error("not found");
      const profile = await res.json();
      setStatus("Selected: " + profile.title + " (ESCO)");
      openDutiesPrompt(profile);
    } catch (_err) {
      setStatus("Selected " + item.title + " — could not load duties template.");
    }
  }

  input.addEventListener("input", () => {
    if (input.value !== lastSelectedTitle) lastSelectedTitle = "";
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => search(input.value), 280);
  });

  input.addEventListener("focus", () => {
    if (input.value.trim().length >= 2 && !suggestions.length) search(input.value);
  });

  input.addEventListener("keydown", (e) => {
    const options = listbox.querySelectorAll('[role="option"]');
    if (listbox.hidden || !options.length) return;
    if (e.key === "ArrowDown") {
      e.preventDefault();
      highlightOption(Math.min(activeIndex + 1, options.length - 1));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      highlightOption(Math.max(activeIndex - 1, 0));
    } else if (e.key === "Enter" && activeIndex >= 0) {
      e.preventDefault();
      selectSuggestion(activeIndex);
    } else if (e.key === "Escape") {
      closeListbox();
    }
  });

  document.addEventListener("click", (e) => {
    if (!e.target.closest(".occupation-combobox")) closeListbox();
  });

  dutiesYes?.addEventListener("click", () => applyDuties("replace"));
  dutiesAppend?.addEventListener("click", () => applyDuties("append"));
  dutiesNo?.addEventListener("click", () => {
    hideMeansBox();
    closeDutiesPrompt();
  });
  dutiesClose?.addEventListener("click", closeDutiesPrompt);
  dutiesBackdrop?.addEventListener("click", closeDutiesPrompt);

  roleConfirmBtn?.addEventListener("click", () => setRoleRequirementsState("confirmed"));
  roleRejectBtn?.addEventListener("click", () => {
    setRoleRequirementsState("rejected");
    roleManualInput?.focus();
  });
  profileSaveBtn?.addEventListener("click", () => saveOccupationProfile());

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && dutiesModal && !dutiesModal.hidden) closeDutiesPrompt();
  });

  restoreSavedProfile();

  gotoOccupationBtn?.addEventListener("click", () => {
    if (window.ClaimBuddyIntake?.goToSectionId) {
      window.ClaimBuddyIntake.goToSectionId("section-occupation");
    }
  });

  if (functionalPlaceholder && functionalBox?.hidden) {
    functionalPlaceholder.hidden = false;
  }
})();