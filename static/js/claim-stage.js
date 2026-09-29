/** Claim stage card picker — syncs to hidden #claim_stage input. */
(function () {
  "use strict";

  var hidden = document.getElementById("claim_stage");
  var status = document.getElementById("claim-stage-status");
  var cards = document.querySelectorAll(".claim-stage-card");
  if (!hidden || !cards.length) return;

  function selectStage(card) {
    if (!card) return;
    var stage = card.getAttribute("data-stage");
    var label = card.getAttribute("data-stage-label") || stage;
    hidden.value = stage;

    cards.forEach(function (c) {
      var on = c === card;
      c.classList.toggle("is-selected", on);
      c.setAttribute("aria-selected", on ? "true" : "false");
    });

    if (status) {
      status.textContent = label + " selected — press Next → when ready.";
    }

    hidden.dispatchEvent(new Event("change", { bubbles: true }));
    document.dispatchEvent(
      new CustomEvent("claim-stage-changed", { detail: { stage: stage, label: label } })
    );
  }

  cards.forEach(function (card) {
    card.addEventListener("click", function () {
      selectStage(card);
    });
  });

  if (hidden.value) {
    var current = document.querySelector(
      '.claim-stage-card[data-stage="' + hidden.value + '"]'
    );
    if (current) selectStage(current);
  }

  window.claimStageState = function () {
    return { stage: hidden.value, ready: !!hidden.value };
  };
})();