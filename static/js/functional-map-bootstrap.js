/** Bootstrap functional map on the standalone functional-capacity module from saved profile JSON. */
(function () {
  const profileHidden = document.getElementById("occupation_profile_json");
  const functionalBox = document.getElementById("functional-duty-map");
  const functionalPlaceholder = document.getElementById("functional-map-placeholder");
  const functionalIntro = document.getElementById("functional-map-intro");
  const functionalGrid = document.getElementById("functional-map-grid");
  if (!functionalGrid || !profileHidden) return;

  function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
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

  function showFunctionalMap(profile) {
    const fmap = profile.functional_map;
    if (!fmap) {
      if (functionalBox) functionalBox.hidden = true;
      if (functionalPlaceholder) functionalPlaceholder.hidden = false;
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

      if (domain.items && domain.items.length) {
        const ul = document.createElement("ul");
        domain.items.forEach((item) => {
          const li = document.createElement("li");
          li.textContent = item;
          ul.appendChild(li);
        });
        card.appendChild(ul);
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
      tokens.forEach((token) => {
        const chip = document.createElement("button");
        chip.type = "button";
        chip.className = "functional-map-illness-chip";
        chip.textContent = token;
        chip.addEventListener("click", (e) => {
          e.stopPropagation();
          dispatchFunctionalSelection(domain.id, domain.illness_link || "", token);
        });
        chipRow.appendChild(chip);
      });
      linkWrap.appendChild(chipRow);
      card.appendChild(linkWrap);

      card.addEventListener("click", () => {
        dispatchFunctionalSelection(domain.id, domain.illness_link || "", "");
      });
      functionalGrid.appendChild(card);
    });

    if (functionalBox) functionalBox.hidden = false;
    if (functionalPlaceholder) functionalPlaceholder.hidden = true;
    document.dispatchEvent(
      new CustomEvent("claimbuddy:functional-map-ready", { detail: { profile } })
    );
  }

  if (!profileHidden.value.trim()) return;
  try {
    const saved = JSON.parse(profileHidden.value);
    if (saved?.functional_map) {
      showFunctionalMap(saved);
    }
  } catch (_e) {
    /* ignore */
  }
})();