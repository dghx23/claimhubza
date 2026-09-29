(function () {
  "use strict";

  var planTypeInput = document.getElementById("policy_plan_type");
  var insurerTileInput = document.getElementById("policy_insurer_tile");
  var insurerField = document.getElementById("insurer");
  var picker = document.getElementById("policy-plan-picker");
  var active = document.getElementById("policy-plan-active");
  var activeLabel = document.getElementById("policy-plan-active-label");
  var groupFlow = document.getElementById("policy-group-flow");
  var privateFlow = document.getElementById("policy-private-flow");
  var uploadWrap = document.getElementById("policy-upload-wrap");
  var uploadSideLabel = document.getElementById("policy-upload-side-label");
  var uploadHeading = document.getElementById("policy-upload-heading");
  var uploadDesc = document.getElementById("policy-upload-desc");
  var insurerChip = document.getElementById("policy-upload-insurer-chip");
  var otherWrap = document.getElementById("policy-insurer-other-wrap");
  var otherInput = document.getElementById("policy_insurer_other");
  var insurerStatus = document.getElementById("policy-insurer-status");
  var changeBtn = document.getElementById("policy-plan-change");

  if (!planTypeInput || !picker) return;

  var tiles = document.querySelectorAll(".insurer-logo-tile");

  function insurerFromTile(tileId) {
    var tile = document.querySelector('.insurer-logo-tile[data-insurer-id="' + tileId + '"]');
    if (!tile) return "";
    if (tileId === "other") {
      return otherInput ? otherInput.value.trim() : "";
    }
    return (
      tile.getAttribute("data-insurer-nfo") ||
      tile.getAttribute("data-insurer-name") ||
      ""
    );
  }

  function syncInsurerField() {
    if (!insurerField) return;
    var plan = planTypeInput.value;
    if (plan === "private" && insurerTileInput && insurerTileInput.value) {
      var name = insurerFromTile(insurerTileInput.value);
      if (!name) return;
      if (typeof window.setInsurerSelectValue === "function") {
        window.setInsurerSelectValue(name);
      } else if (insurerField.tagName === "SELECT") {
        var found = false;
        Array.prototype.forEach.call(insurerField.options, function (opt) {
          if (opt.value === name) {
            insurerField.value = name;
            found = true;
          }
        });
        if (!found) insurerField.value = "__other__";
      } else {
        insurerField.value = name;
      }
    }
  }

  function updateInsurerChip(tile) {
    if (!insurerChip) return;
    if (!tile) {
      insurerChip.textContent = "Insurer";
      insurerChip.style.removeProperty("--insurer-accent");
      return;
    }
    var mark = tile.querySelector(".insurer-logo-mark");
    var name = tile.getAttribute("data-insurer-name") || "Insurer";
    var accent = tile.style.getPropertyValue("--insurer-accent");
    insurerChip.textContent = mark ? mark.textContent + " · " + name : name;
    if (accent) insurerChip.style.setProperty("--insurer-accent", accent);
  }

  function updateInsurerStatus(tileId) {
    if (!insurerStatus) return;
    if (!tileId) {
      insurerStatus.textContent = "";
      return;
    }
    var name = insurerFromTile(tileId);
    if (tileId === "other" && !name) {
      insurerStatus.textContent = "Enter your insurer name below.";
      return;
    }
    insurerStatus.textContent = name
      ? "Selected: " + name + " — upload your policy wording next."
      : "";
  }

  function setUploadCopy(plan) {
    if (uploadHeading) {
      uploadHeading.textContent =
        plan === "group" ? "Upload group policy" : "Upload policy";
    }
    if (uploadDesc) {
      uploadDesc.textContent =
        plan === "group"
          ? "Employer benefits booklet, group schedule, or member certificate."
          : "Policy wording, schedule, or member certificate.";
    }
  }

  function setUploadVisibility(plan, opts) {
    opts = opts || {};
    if (!uploadWrap) return;

    var show =
      plan === "group" ||
      (plan === "private" &&
        insurerTileInput &&
        insurerTileInput.value &&
        (insurerTileInput.value !== "other" ||
          (otherInput && otherInput.value.trim())));

    if (opts.hasExistingPolicy) show = true;

    uploadWrap.hidden = !show;
    if (uploadSideLabel) uploadSideLabel.hidden = plan !== "private";
    setUploadCopy(plan);
  }

  function setUploadContext(plan) {
    if (!uploadWrap) return;
    uploadWrap.classList.toggle("policy-upload-wrap--group", plan === "group");
    uploadWrap.classList.toggle("policy-upload-wrap--private", plan === "private");
  }

  function showPlan(plan, opts) {
    opts = opts || {};
    planTypeInput.value = plan;

    picker.hidden = true;
    active.hidden = false;

    if (groupFlow) groupFlow.hidden = plan !== "group";
    if (privateFlow) privateFlow.hidden = plan !== "private";
    setUploadContext(plan);

    if (activeLabel) {
      activeLabel.textContent =
        plan === "group"
          ? "Group plan — employer or scheme policy"
          : "Private plan — individual policy";
    }

    if (plan === "group") {
      if (insurerTileInput) insurerTileInput.value = "";
      tiles.forEach(function (t) {
        t.classList.remove("is-selected");
        t.setAttribute("aria-pressed", "false");
        t.setAttribute("aria-selected", "false");
      });
      if (otherWrap) otherWrap.hidden = true;
      if (otherInput) otherInput.value = "";
      updateInsurerChip(null);
      updateInsurerStatus("");
    }

    setUploadVisibility(plan, opts);

    if (!opts.skipEvent) {
      document.dispatchEvent(
        new CustomEvent("policy-plan-changed", { detail: { planType: plan } })
      );
    }
  }

  function resetPlan() {
    planTypeInput.value = "";
    if (insurerTileInput) insurerTileInput.value = "";
    picker.hidden = false;
    active.hidden = true;
    if (groupFlow) groupFlow.hidden = true;
    if (privateFlow) privateFlow.hidden = true;
    if (uploadWrap) uploadWrap.hidden = true;
    tiles.forEach(function (t) {
      t.classList.remove("is-selected");
      t.setAttribute("aria-pressed", "false");
      t.setAttribute("aria-selected", "false");
    });
    if (otherWrap) otherWrap.hidden = true;
    if (otherInput) otherInput.value = "";
    updateInsurerChip(null);
    updateInsurerStatus("");
    setUploadContext("");
    document.dispatchEvent(
      new CustomEvent("policy-plan-changed", { detail: { planType: "" } })
    );
  }

  function selectInsurerTile(tile) {
    if (!tile || !insurerTileInput) return;
    var id = tile.getAttribute("data-insurer-id");
    insurerTileInput.value = id;

    tiles.forEach(function (t) {
      var on = t === tile;
      t.classList.toggle("is-selected", on);
      t.setAttribute("aria-pressed", on ? "true" : "false");
      t.setAttribute("aria-selected", on ? "true" : "false");
    });

    if (otherWrap) {
      otherWrap.hidden = id !== "other";
      if (id !== "other" && otherInput) otherInput.value = "";
    }

    updateInsurerChip(tile);
    updateInsurerStatus(id);
    syncInsurerField();
    setUploadVisibility("private");

    document.dispatchEvent(
      new CustomEvent("policy-insurer-selected", { detail: { insurerId: id } })
    );
  }

  document.querySelectorAll(".policy-plan-card").forEach(function (card) {
    card.addEventListener("click", function () {
      var plan = card.getAttribute("data-plan-type");
      if (plan) showPlan(plan);
    });
  });

  if (changeBtn) {
    changeBtn.addEventListener("click", resetPlan);
  }

  tiles.forEach(function (tile) {
    tile.addEventListener("click", function () {
      selectInsurerTile(tile);
    });
  });

  if (otherInput) {
    otherInput.addEventListener("input", function () {
      if (insurerTileInput && insurerTileInput.value === "other") {
        syncInsurerField();
        updateInsurerStatus("other");
        setUploadVisibility("private");
      }
    });
  }

  function restoreFromClaim() {
    var plan = planTypeInput.value;
    if (!plan) return;

    var previewList = document.getElementById("policy-preview-list");
    var hasExisting =
      !!document.querySelector(".uploaded-job-specs li") ||
      !!(previewList && previewList.children && previewList.children.length);

    showPlan(plan, { skipEvent: true, hasExistingPolicy: hasExisting });

    if (plan === "private" && insurerField && insurerTileInput) {
      var saved = (insurerField.value || "").trim();
      if (!saved) return;

      var matched = false;
      tiles.forEach(function (tile) {
        var nfo = (tile.getAttribute("data-insurer-nfo") || "").trim();
        var short = (tile.getAttribute("data-insurer-name") || "").trim();
        if (
          (nfo && saved.toLowerCase() === nfo.toLowerCase()) ||
          (short && saved.toLowerCase() === short.toLowerCase())
        ) {
          selectInsurerTile(tile);
          matched = true;
        }
      });

      if (!matched) {
        var otherTile = document.querySelector('.insurer-logo-tile[data-insurer-id="other"]');
        if (otherTile) {
          selectInsurerTile(otherTile);
          if (otherInput) otherInput.value = saved;
          updateInsurerStatus("other");
          setUploadVisibility("private", { hasExistingPolicy: hasExisting });
        }
      }
    }
  }

  restoreFromClaim();

  window.policyPlanState = function () {
    var plan = planTypeInput.value;
    var tile = insurerTileInput ? insurerTileInput.value : "";
    var otherName =
      tile === "other" && otherInput ? otherInput.value.trim() : "";
    return {
      planType: plan,
      insurerTile: tile,
      insurerName: insurerField ? insurerField.value.trim() : "",
      otherInsurer: otherName,
      ready:
        plan === "group" ||
        (plan === "private" && tile && (tile !== "other" || !!otherName)),
    };
  };
})();