/** Auto-save functional-capacity data from the standalone module (synced with intake). */
(function () {
  const configEl = document.getElementById("functional-capacity-config");
  if (!configEl) return;

  let config = {};
  try {
    config = JSON.parse(configEl.textContent || "{}");
  } catch (e) {
    return;
  }
  if (!config.save_url) return;

  const fcHidden = document.getElementById("functional_capacity_json");
  const illnessSummary = document.getElementById("illness_summary");
  const statusEl = document.getElementById("functional-sync-status");
  let timer = null;
  let saving = false;
  let pending = false;

  function setStatus(text, kind) {
    if (!statusEl) return;
    statusEl.textContent = text ? " · " + text : "";
    statusEl.className = "functional-sync-status" + (kind ? " functional-sync-status--" + kind : "");
  }

  async function saveNow() {
    if (saving) {
      pending = true;
      return;
    }
    saving = true;
    setStatus("Saving…", "pending");

    const payload = {
      functional_capacity_json: fcHidden?.value || "",
      illness_summary: illnessSummary?.value || "",
    };

    try {
      const res = await fetch(config.save_url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!res.ok) throw new Error("save failed");
      setStatus("Saved", "ok");
      window.setTimeout(() => setStatus("", ""), 2500);
    } catch (e) {
      setStatus("Save failed — retry when online", "error");
    } finally {
      saving = false;
      if (pending) {
        pending = false;
        saveNow();
      }
    }
  }

  function scheduleSave() {
    window.clearTimeout(timer);
    timer = window.setTimeout(saveNow, 600);
  }

  fcHidden?.addEventListener("change", scheduleSave);
  illnessSummary?.addEventListener("input", scheduleSave);

  if (config.initial_domain) {
    document.addEventListener("claimbuddy:functional-map-ready", () => {
      document.dispatchEvent(
        new CustomEvent("claimbuddy:select-functional-domain", {
          detail: { domainId: config.initial_domain },
        })
      );
    });
    window.setTimeout(() => {
      document.dispatchEvent(
        new CustomEvent("claimbuddy:select-functional-domain", {
          detail: { domainId: config.initial_domain },
        })
      );
    }, 400);
  }
})();