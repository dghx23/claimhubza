/** Policy upload modal + cross-link analysis across intake form. */
(function () {
  const ALLOWED_EXT = [".pdf", ".doc", ".docx", ".txt", ".png", ".jpg", ".jpeg"];
  const MAX_BYTES = 32 * 1024 * 1024;

  const FIELD_LABELS = {
    waiting_period: "Waiting period",
    benefit_percent: "Insured benefit %",
    gross_salary: "Gross earnings",
    date_of_absence: "Date of Absence",
    insurer_doa: "Insurer-stated DOA",
    occupation: "Occupation",
    material_duties: "Material duties",
    illness_summary: "Illness / injury summary",
    first_notice: "First notice",
    form_submission: "Form submission",
    complete_claim: "Complete claim",
    other_deductions: "Other deductions",
    salary_notes: "Deduction notes",
    review_deadline: "Review deadline",
    ombud_deadline: "Ombud deadline",
    cover_start: "Cover start",
    policy_number: "Policy number",
    policyholder: "Policyholder",
    insurer: "Insurer",
    employer: "Employer",
    notes: "Notes",
    medical_aid_deductions: "Medical aid",
    pension_deductions: "Pension / provident fund",
    uif_deductions: "UIF",
    tax_deductions: "PAYE / tax",
    hospital_admission: "Hospital admission",
    specialist_required: "Specialist evidence",
  };

  const AUTO_FILL_PARTY_FIELDS = [
    "policy_number",
    "policyholder",
    "insurer",
    "employer",
  ];

  const EVIDENCE_FLAG_FIELDS = ["hospital_admission", "specialist_required"];

  const EVIDENCE_FLAG_STATIC_HELP = {
    hospital_admission:
      "<p class='policy-hint-guidance'><strong>What ClaimBuddy does:</strong> Adds hospital admission/discharge records to your evidence gaps and flags the <em>diagnosis trap</em>.</p>",
    specialist_required:
      "<p class='policy-hint-guidance'><strong>What ClaimBuddy does:</strong> Prioritises specialist letters on your evidence list and flags the <em>specialist-evidence trap</em>.</p>",
  };

  const HINT_STATUS_LABELS = {
    covered: "Covered",
    excluded: "Excluded",
    offset: "Offset / integration",
    employer_paid: "Employer-paid",
    mentioned: "Mentioned",
  };

  const SECTION_ANCHORS = {
    "Parties & key dates": "section-parties",
    Occupation: "section-occupation",
    "Health story": "section-health-story",
    "Occupation & health": "section-occupation",
    "Salary & deductions": "section-salary",
    "Key dates": "section-dates",
    Notes: "section-notes",
  };

  function gotoIntakeSection(sectionId, focusFieldId) {
    if (window.ClaimBuddyIntake?.goToSectionId) {
      window.ClaimBuddyIntake.goToSectionId(sectionId, focusFieldId);
      return;
    }
    document.dispatchEvent(
      new CustomEvent("claimbuddy:intake-goto", {
        detail: { sectionId, focusFieldId },
      })
    );
  }

  const modal = document.getElementById("policy-modal");
  const backdrop = document.getElementById("policy-modal-backdrop");
  const openBtns = document.querySelectorAll(".policy-open, #policy-open");
  const closeBtn = document.getElementById("policy-close");
  const doneBtn = document.getElementById("policy-done");
  const browseBtn = document.getElementById("policy-browse");
  const dropzone = document.getElementById("policy-dropzone");
  const fileInput = document.getElementById("policy");
  const modalList = document.getElementById("policy-modal-list");
  const previewList = document.getElementById("policy-preview-list");
  const previewEmpty = document.getElementById("policy-preview-empty");
  const previewCount = document.getElementById("policy-preview-count");
  const analyzeStatus = document.getElementById("policy-analyze-status");
  const crossLinkBox = document.getElementById("policy-cross-link");
  const crossLinkTitle = document.getElementById("policy-cross-link-title");
  const crossLinkSub = document.getElementById("policy-cross-link-sub");
  const crossLinkBody = document.getElementById("policy-cross-link-body");
  const suggestedBox = document.getElementById("policy-suggested");
  const trapsBox = document.getElementById("policy-traps");
  const hiddenJson = document.getElementById("policy_analysis_json");

  if (!fileInput) return;

  let pendingFiles = [];
  let currentAnalysis = null;
  let analyzing = false;

  function extOf(name) {
    const i = name.lastIndexOf(".");
    return i >= 0 ? name.slice(i).toLowerCase() : "";
  }

  function formatSize(bytes) {
    if (bytes < 1024) return bytes + " B";
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
    return (bytes / (1024 * 1024)).toFixed(1) + " MB";
  }

  function validate(file) {
    const ext = extOf(file.name);
    if (!ALLOWED_EXT.includes(ext)) {
      return "File type " + ext + " not allowed for " + file.name;
    }
    if (file.size > MAX_BYTES) {
      return file.name + " exceeds 32 MB limit";
    }
    return null;
  }

  function fileKey(file) {
    return file.name + "|" + file.size + "|" + file.lastModified;
  }

  function syncInput() {
    const dt = new DataTransfer();
    pendingFiles.forEach((f) => dt.items.add(f));
    fileInput.files = dt.files;
  }

  function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }

  function renderFileList(container, removable) {
    if (!container) return;
    container.innerHTML = "";
    if (!pendingFiles.length) {
      const empty = document.createElement("li");
      empty.className = "job-spec-empty-item";
      empty.textContent = removable
        ? "No policy selected — drag files here or browse."
        : "No new policy selected.";
      container.appendChild(empty);
      return;
    }
    pendingFiles.forEach((file, index) => {
      const li = document.createElement("li");
      li.className = "job-spec-file-item";
      const icon = document.createElement("span");
      icon.className = "job-spec-file-icon";
      icon.textContent = "📋";
      const meta = document.createElement("span");
      meta.className = "job-spec-file-meta";
      meta.innerHTML =
        "<strong>" +
        escapeHtml(file.name) +
        "</strong><span>" +
        formatSize(file.size) +
        "</span>";
      li.appendChild(icon);
      li.appendChild(meta);
      if (removable) {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "btn btn-danger btn-tiny job-spec-remove";
        btn.textContent = "Remove";
        btn.addEventListener("click", () => {
          pendingFiles.splice(index, 1);
          syncInput();
          renderAll();
          if (pendingFiles.length) {
            analyzeFile(pendingFiles[pendingFiles.length - 1]);
          } else {
            clearAnalysis();
          }
        });
        li.appendChild(btn);
      }
      container.appendChild(li);
    });
  }

  function updatePreview() {
    const n = pendingFiles.length;
    if (previewCount) {
      previewCount.textContent = n
        ? n + " polic" + (n === 1 ? "y" : "ies") + " ready to upload"
        : "";
      previewCount.hidden = !n;
    }
    if (previewEmpty) previewEmpty.hidden = n > 0;
    if (previewList) {
      if (n) renderFileList(previewList, false);
      else previewList.innerHTML = "";
    }
  }

  function renderAll() {
    renderFileList(modalList, true);
    updatePreview();
  }

  function setStatus(msg, isError) {
    if (!analyzeStatus) return;
    analyzeStatus.textContent = msg || "";
    analyzeStatus.classList.toggle("policy-analyze-error", !!isError);
    analyzeStatus.classList.toggle("policy-analyze-ok", !!msg && !isError);
  }

  function clearFieldHighlights() {
    document.querySelectorAll(".policy-linked").forEach((el) => {
      el.classList.remove("policy-linked");
    });
    document.querySelectorAll(".policy-linked-field").forEach((el) => {
      el.classList.remove("policy-linked-field");
    });
  }

  function evidenceFlagWrap(el) {
    return el?.closest(".claim-evidence-flag") || el?.closest(".field");
  }

  function highlightFields(fieldIds) {
    clearFieldHighlights();
    const unique = [...new Set(fieldIds)];
    unique.forEach((id) => {
      let el = document.getElementById(id);
      if (id === "waiting_period") {
        el = document.getElementById("waiting_period_select") || el;
      }
      if (el) {
        el.classList.add("policy-linked");
        const wrap = evidenceFlagWrap(el);
        if (wrap) wrap.classList.add("policy-linked-field");
      }
    });
  }

  function persistAnalysis(analysis) {
    currentAnalysis = analysis;
    if (hiddenJson && analysis) {
      hiddenJson.value = JSON.stringify(analysis);
    }
  }

  function findLabelForField(fieldId) {
    if (fieldId === "waiting_period") {
      return document.querySelector(".waiting-period-field label");
    }
    const direct = document.querySelector('label[for="' + fieldId + '"]');
    if (direct) return direct;
    return document.getElementById("label-" + fieldId);
  }

  function clearFieldHints() {
    document.querySelectorAll(".policy-hint-wrap[data-hint-for]").forEach((el) => el.remove());
    document.querySelectorAll(".policy-hint-active").forEach((el) => {
      if (!el.querySelector(".policy-hint-wrap[data-static-help]")) {
        el.classList.remove("policy-hint-active");
      }
    });
    resetEvidenceFlagsFromPolicy();
  }

  function resetEvidenceFlagsFromPolicy() {
    EVIDENCE_FLAG_FIELDS.forEach((fieldId) => {
      const desc = document.getElementById(fieldId + "-desc");
      if (desc && desc.dataset.defaultDesc) {
        desc.textContent = desc.dataset.defaultDesc;
        desc.classList.remove("claim-evidence-flag-desc--from-policy");
      }
      const popover = document.getElementById(fieldId + "-hint-popover");
      if (popover && popover.dataset.defaultHtml) {
        popover.innerHTML = popover.dataset.defaultHtml;
      }
      const label = findLabelForField(fieldId);
      if (label && !label.querySelector(".policy-hint-wrap[data-hint-for]")) {
        label.classList.remove("policy-hint-active");
      }
    });
  }

  function buildEvidenceFlagPopover(fieldId, hint) {
    const status = HINT_STATUS_LABELS[hint.status] || hint.status_label || "Policy";
    const staticHelp = EVIDENCE_FLAG_STATIC_HELP[fieldId] || "";
    return (
      "<strong>" +
      escapeHtml(hint.topic || "Specialist evidence") +
      " — from your policy</strong>" +
      "<span class='policy-hint-status policy-hint-status-" +
      escapeHtml(hint.status || "mentioned") +
      "'>" +
      escapeHtml(hint.status_label || status) +
      "</span>" +
      (hint.detail
        ? "<p class='policy-hint-quote'>“" + escapeHtml(hint.detail) + "”</p>"
        : "") +
      (hint.guidance
        ? "<p class='policy-hint-guidance'>" + escapeHtml(hint.guidance) + "</p>"
        : "") +
      staticHelp
    );
  }

  function applyEvidenceFlagFromPolicy(fieldId, hint) {
    if (!hint || !hint.found) return false;
    const checkbox = document.getElementById(fieldId);
    const desc = document.getElementById(fieldId + "-desc");
    const popover = document.getElementById(fieldId + "-hint-popover");
    const label = findLabelForField(fieldId);
    if (!checkbox) return false;

    checkbox.checked = true;
    checkbox.classList.add("policy-linked");
    const wrap = evidenceFlagWrap(checkbox);
    if (wrap) wrap.classList.add("policy-linked-field");
    if (label) label.classList.add("policy-hint-active");

    if (desc) {
      const lead = hint.detail
        ? "From your policy: “" + hint.detail + "”"
        : "Your policy references " + (hint.topic || "this requirement") + ".";
      desc.textContent = lead;
      desc.classList.add("claim-evidence-flag-desc--from-policy");
    }

    if (popover) {
      if (!popover.dataset.defaultHtml) {
        popover.dataset.defaultHtml = popover.innerHTML;
      }
      popover.innerHTML = buildEvidenceFlagPopover(fieldId, hint);
    }

    return true;
  }

  function applyEvidenceFlagsFromPolicy(analysis) {
    const hints = analysis?.field_hints || {};
    const flags = analysis?.evidence_flags || {};
    const applied = [];
    EVIDENCE_FLAG_FIELDS.forEach((fieldId) => {
      if (!flags[fieldId] && !hints[fieldId]?.found) return;
      if (applyEvidenceFlagFromPolicy(fieldId, hints[fieldId])) {
        applied.push(FIELD_LABELS[fieldId] || fieldId);
      }
    });
    return applied;
  }

  function buildHintPopover(hint) {
    const status = HINT_STATUS_LABELS[hint.status] || hint.status_label || "Policy";
    return (
      "<strong>" +
      escapeHtml(hint.topic || "Policy coverage") +
      "</strong>" +
      "<span class='policy-hint-status policy-hint-status-" +
      escapeHtml(hint.status || "mentioned") +
      "'>" +
      escapeHtml(hint.status_label || status) +
      "</span>" +
      (hint.detail
        ? "<p class='policy-hint-quote'>“" + escapeHtml(hint.detail) + "”</p>"
        : "") +
      (hint.guidance
        ? "<p class='policy-hint-guidance'>" + escapeHtml(hint.guidance) + "</p>"
        : "")
    );
  }

  function attachHintToLabel(label, fieldId, hint) {
    if (EVIDENCE_FLAG_FIELDS.includes(fieldId)) return;
    if (!label || label.querySelector(".policy-hint-wrap")) return;
    const wrap = document.createElement("span");
    wrap.className = "policy-hint-wrap";
    wrap.dataset.hintFor = fieldId;
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "policy-hint-btn";
    btn.setAttribute("aria-label", "Policy coverage details for " + (hint.topic || fieldId));
    btn.textContent = "?";
    const popover = document.createElement("span");
    popover.className = "policy-hint-popover";
    popover.setAttribute("role", "tooltip");
    popover.innerHTML = buildHintPopover(hint);
    wrap.appendChild(btn);
    wrap.appendChild(popover);
    if (label.classList.contains("checkbox-label-with-hint")) {
      const textSpan = label.querySelector(".checkbox-label-text");
      if (textSpan) textSpan.appendChild(wrap);
      else label.appendChild(wrap);
    } else {
      label.appendChild(document.createTextNode(" "));
      label.appendChild(wrap);
    }
    label.classList.add("policy-hint-active");
    const field = document.getElementById(fieldId);
    if (field) {
      field.classList.add("policy-linked");
      const fieldWrap = field.closest(".field");
      if (fieldWrap) fieldWrap.classList.add("policy-linked-field");
    }
  }

  function applyFieldHints(analysis) {
    clearFieldHints();
    const hints = analysis?.field_hints || {};
    Object.entries(hints).forEach(([fieldId, hint]) => {
      if (!hint || !hint.found) return;
      const label = findLabelForField(fieldId);
      attachHintToLabel(label, fieldId, hint);
    });
  }

  function clearAnalysis() {
    currentAnalysis = null;
    if (hiddenJson) hiddenJson.value = "";
    if (crossLinkBox) crossLinkBox.hidden = true;
    clearFieldHighlights();
    clearFieldHints();
    setStatus("");
  }

  const INVALID_PARTY_TOKENS = new Set([
    "which", "under", "means", "the", "this", "that", "shall", "will", "any", "all",
  ]);
  const PARTY_BOILERPLATE =
    /\b(employment|contract|legal|document|specifies|defined|definition|agreement|schedule)\b/i;

  function isPlausiblePartyValue(fieldId, value) {
    const v = String(value || "").trim();
    if (!v) return false;
    if (fieldId === "policy_number") {
      if (v.length < 4 || !/\d/.test(v) || INVALID_PARTY_TOKENS.has(v.toLowerCase())) {
        return false;
      }
      if (!/^[A-Za-z0-9][A-Za-z0-9\s\-/.]*$/.test(v)) return false;
    } else {
      if (v.length < 3 || PARTY_BOILERPLATE.test(v)) return false;
      if (/^(and|or|the|any|which|under|means)\b/i.test(v)) return false;
      if (v.split(/\s+/).length > 7) return false;
    }
    return true;
  }

  function isFieldEmpty(fieldId) {
    const el = document.getElementById(fieldId);
    return !el || !String(el.value || "").trim();
  }

  function markFieldLinked(fieldId) {
    let el = document.getElementById(fieldId);
    if (fieldId === "waiting_period") {
      el = document.getElementById("waiting_period_select") || el;
    }
    if (el) el.classList.add("policy-linked");
    const wrap =
      evidenceFlagWrap(el) ||
      document.getElementById("waiting_period_select")?.closest(".field");
    if (wrap) wrap.classList.add("policy-linked-field");
  }

  function applySuggestedValue(fieldId, value, onlyIfEmpty) {
    if (!value) return false;
    if (AUTO_FILL_PARTY_FIELDS.includes(fieldId) && !isPlausiblePartyValue(fieldId, value)) {
      return false;
    }
    if (onlyIfEmpty && !isFieldEmpty(fieldId)) return false;
    if (fieldId === "waiting_period" && window.setWaitingPeriodValue) {
      window.setWaitingPeriodValue(value);
    } else {
      const field = document.getElementById(fieldId);
      if (!field) return false;
      field.value = value;
      field.dispatchEvent(new Event("change", { bubbles: true }));
    }
    markFieldLinked(fieldId);
    return true;
  }

  function autoApplyParties(analysis) {
    const parties = analysis.parties || {};
    const suggested = analysis.suggested || {};
    const filled = [];
    AUTO_FILL_PARTY_FIELDS.forEach((fieldId) => {
      const value = parties[fieldId] || suggested[fieldId];
      if (applySuggestedValue(fieldId, value, true)) {
        filled.push(FIELD_LABELS[fieldId] || fieldId);
      }
    });
    return filled;
  }

  function renderCrossLinks(analysis) {
    if (!crossLinkBox || !analysis || !analysis.processed) {
      if (crossLinkBox) crossLinkBox.hidden = true;
      return [];
    }

    const matched = analysis.terms_matched || 0;
    const filename = analysis.filename || "policy document";
    const pages = analysis.pages ? " · " + analysis.pages + " page" + (analysis.pages === 1 ? "" : "s") : "";

    if (crossLinkTitle) {
      crossLinkTitle.textContent = "Policy linked across your intake";
    }
    if (crossLinkSub) {
      crossLinkSub.textContent =
        matched +
        " clause area" +
        (matched === 1 ? "" : "s") +
        " found in " +
        filename +
        pages +
        " — jump to the fields below.";
    }

    if (suggestedBox) {
      const suggested = analysis.suggested || {};
      const keys = Object.keys(suggested);
      if (keys.length) {
        suggestedBox.hidden = false;
        suggestedBox.innerHTML =
          "<strong>Suggested from policy text</strong><ul class='policy-suggested-list'>" +
          keys
            .map((key) => {
              const label = FIELD_LABELS[key] || key;
              return (
                "<li><span>" +
                escapeHtml(label) +
                ": <em>" +
                escapeHtml(suggested[key]) +
                "</em></span> " +
                "<button type='button' class='btn btn-secondary btn-tiny policy-apply' data-field='" +
                escapeHtml(key) +
                "' data-value='" +
                escapeHtml(suggested[key]) +
                "'>Apply</button></li>"
              );
            })
            .join("") +
          "</ul>";
        suggestedBox.querySelectorAll(".policy-apply").forEach((btn) => {
          btn.addEventListener("click", () => {
            applySuggestedValue(btn.dataset.field, btn.dataset.value, true);
          });
        });
      } else {
        suggestedBox.hidden = true;
        suggestedBox.innerHTML = "";
      }
    }

    if (trapsBox) {
      const traps = analysis.traps || [];
      if (traps.length) {
        trapsBox.hidden = false;
        trapsBox.innerHTML =
          "<strong>Policy traps to watch</strong><ul class='policy-traps-list'>" +
          traps.map((t) => "<li>" + escapeHtml(t) + "</li>").join("") +
          "</ul>";
      } else {
        trapsBox.hidden = true;
        trapsBox.innerHTML = "";
      }
    }

    if (crossLinkBody) {
      const links = analysis.cross_links || [];
      if (!links.length) {
        crossLinkBody.innerHTML =
          "<p class='policy-cross-link-empty'>No standard clause headings detected — you can still complete the form manually.</p>";
      } else {
        crossLinkBody.innerHTML = links
          .map((group) => {
            const anchor = SECTION_ANCHORS[group.section] || "#";
            const items = (group.items || [])
              .map((item) => {
                const fieldLinks = (item.fields || [])
                  .map((fid) => {
                    const label = FIELD_LABELS[fid] || fid;
                    return (
                      "<a href='#" +
                      escapeHtml(fid) +
                      "' class='policy-field-link' data-field='" +
                      escapeHtml(fid) +
                      "'>" +
                      escapeHtml(label) +
                      "</a>"
                    );
                  })
                  .join(", ");
                const snippet = item.snippet
                  ? "<p class='policy-snippet'>“" + escapeHtml(item.snippet) + "”</p>"
                  : "";
                return (
                  "<li><strong>" +
                  escapeHtml(item.term) +
                  "</strong> → " +
                  fieldLinks +
                  snippet +
                  "</li>"
                );
              })
              .join("");
            return (
              "<div class='policy-cross-group'>" +
              "<h4><a href='#" +
              anchor +
              "' class='policy-section-link' data-section-id='" +
              anchor +
              "'>" +
              escapeHtml(group.section) +
              "</a></h4>" +
              "<ul>" +
              items +
              "</ul></div>"
            );
          })
          .join("");
      }

      crossLinkBody.querySelectorAll(".policy-section-link").forEach((link) => {
        link.addEventListener("click", (e) => {
          e.preventDefault();
          const sectionId = link.dataset.sectionId;
          if (sectionId) gotoIntakeSection(sectionId);
        });
      });

      crossLinkBody.querySelectorAll(".policy-field-link").forEach((link) => {
        link.addEventListener("click", (e) => {
          e.preventDefault();
          const id = link.dataset.field;
          const el = document.getElementById(id);
          if (!el) return;
          const section = el.closest(".intake-screen");
          const sectionId = section?.id;
          highlightFields([id]);
          if (sectionId) gotoIntakeSection(sectionId, id);
          else {
            el.scrollIntoView({ behavior: "smooth", block: "center" });
            el.focus({ preventScroll: true });
          }
        });
      });
    }

    const allFields = [];
    (analysis.cross_links || []).forEach((g) => {
      (g.items || []).forEach((item) => {
        (item.fields || []).forEach((f) => allFields.push(f));
      });
    });
    highlightFields(allFields);
    applyFieldHints(analysis);
    const evidenceFilled = applyEvidenceFlagsFromPolicy(analysis);
    crossLinkBox.hidden = false;
    const partyFilled = autoApplyParties(analysis) || [];
    return partyFilled.concat(evidenceFilled);
  }

  async function analyzeFile(file) {
    if (!file || analyzing) return;
    analyzing = true;
    setStatus("Scanning policy for clause links…");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("/api/policy/analyze", { method: "POST", body: formData });
      const data = await res.json();
      if (!res.ok) {
        setStatus(data.error || "Analysis failed", true);
        return;
      }
      if (data.error && !data.processed) {
        setStatus(data.error, true);
        persistAnalysis(data);
        renderCrossLinks(data);
        return;
      }
      persistAnalysis(data);
      const filled = renderCrossLinks(data) || [];
      const n = data.terms_matched || 0;
      let msg =
        "Processed " +
        file.name +
        " — " +
        n +
        " clause area" +
        (n === 1 ? "" : "s") +
        " linked across the form.";
      if (filled.length) {
        msg += " Auto-filled: " + filled.join(", ") + ".";
      }
      setStatus(msg);
    } catch (err) {
      setStatus("Could not analyze policy — check connection and try again.", true);
    } finally {
      analyzing = false;
    }
  }

  function addFiles(fileList) {
    const errors = [];
    let added = null;
    Array.from(fileList || []).forEach((file) => {
      const err = validate(file);
      if (err) {
        errors.push(err);
        return;
      }
      const key = fileKey(file);
      if (pendingFiles.some((f) => fileKey(f) === key)) return;
      pendingFiles.push(file);
      added = file;
    });
    syncInput();
    renderAll();
    if (errors.length) alert(errors.join("\n"));
    if (added) analyzeFile(added);
  }

  function openModal() {
    if (!modal) return;
    modal.hidden = false;
    backdrop.hidden = false;
    document.body.classList.add("modal-open");
    dropzone?.classList.remove("is-dragover");
  }

  function closeModal() {
    if (!modal) return;
    modal.hidden = true;
    backdrop.hidden = true;
    document.body.classList.remove("modal-open");
    dropzone?.classList.remove("is-dragover");
  }

  openBtns.forEach((btn) => btn.addEventListener("click", openModal));
  closeBtn?.addEventListener("click", closeModal);
  doneBtn?.addEventListener("click", closeModal);
  backdrop?.addEventListener("click", closeModal);
  browseBtn?.addEventListener("click", () => fileInput.click());

  fileInput.addEventListener("change", () => addFiles(fileInput.files));

  if (dropzone) {
    ["dragenter", "dragover"].forEach((evt) => {
      dropzone.addEventListener(evt, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropzone.classList.add("is-dragover");
      });
    });
    ["dragleave", "drop"].forEach((evt) => {
      dropzone.addEventListener(evt, (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (evt === "drop") addFiles(e.dataTransfer.files);
        dropzone.classList.remove("is-dragover");
      });
    });
  }

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && modal && !modal.hidden) closeModal();
  });

  const bootstrap = document.getElementById("policy-analysis-bootstrap");
  if (bootstrap && bootstrap.textContent.trim()) {
    try {
      const analysis = JSON.parse(bootstrap.textContent);
      persistAnalysis(analysis);
      const filled = renderCrossLinks(analysis) || [];
      if (analysis.filename) {
        let msg = "Loaded saved policy analysis from " + analysis.filename + ".";
        if (filled.length) msg += " Auto-filled: " + filled.join(", ") + ".";
        setStatus(msg);
      }
    } catch (e) {
      /* ignore invalid bootstrap */
    }
  }

  renderAll();
})();