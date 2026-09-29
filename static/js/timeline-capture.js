/** Structured quick-timeline date pickers — exact, month+year, or year-only. */
(function () {
  const root = document.getElementById("illness-timeline-capture");
  if (!root) return;

  const MONTH_NAMES = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
  ];

  const currentYear = new Date().getFullYear();

  function populateYearSelect(select) {
    if (!select || select.options.length > 1) return;
    for (let y = currentYear + 1; y >= 1990; y -= 1) {
      const opt = document.createElement("option");
      opt.value = String(y);
      opt.textContent = String(y);
      select.appendChild(opt);
    }
  }

  function formatExactDate(iso) {
    if (!iso) return "";
    const parts = iso.split("-");
    if (parts.length !== 3) return iso;
    const y = Number(parts[0]);
    const m = Number(parts[1]) - 1;
    const d = Number(parts[2]);
    const dt = new Date(y, m, d);
    if (Number.isNaN(dt.getTime())) return iso;
    return dt.toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" });
  }

  function setPickerVisibility(field, precision) {
    field.querySelector(".timeline-picker-exact").hidden = precision !== "exact";
    field.querySelector(".timeline-picker-month").hidden = precision !== "month";
    field.querySelector(".timeline-picker-year").hidden = precision !== "year";
  }

  function readField(field) {
    const id = field.dataset.timelineId || "";
    const label = field.querySelector("label")?.textContent?.trim() || id;
    const precision = field.querySelector(".timeline-precision")?.value || "exact";
    const previewEl = field.querySelector(".timeline-date-preview");

    let display = "";
    let iso = "";
    let complete = false;
    let approx = false;

    if (precision === "exact") {
      iso = field.querySelector(".timeline-date-exact")?.value || "";
      complete = !!iso;
      display = complete ? formatExactDate(iso) : "";
    } else if (precision === "month") {
      const month = field.querySelector(".timeline-month")?.value || "";
      const year = field.querySelector(".timeline-year-month")?.value || "";
      complete = !!(month && year);
      approx = complete;
      if (complete) {
        iso = year + "-" + month + "-01";
        const monthName = MONTH_NAMES[Number(month) - 1] || month;
        display = monthName + " " + year + " (approx)";
      }
    } else if (precision === "year") {
      const year = field.querySelector(".timeline-year-only")?.value || "";
      complete = !!year;
      approx = complete;
      if (complete) {
        iso = year + "-01-01";
        display = year + " (approx)";
      }
    }

    const anyInput =
      field.querySelector(".timeline-date-exact")?.value ||
      field.querySelector(".timeline-month")?.value ||
      field.querySelector(".timeline-year-month")?.value ||
      field.querySelector(".timeline-year-only")?.value;

    if (previewEl) {
      previewEl.textContent = display ? "Selected: " + display : "";
      previewEl.classList.toggle("is-empty", !display);
    }

    field.classList.toggle("is-incomplete", !!anyInput && !complete);
    field.classList.toggle("has-value", complete);

    return {
      id,
      label,
      precision,
      display,
      iso,
      complete,
      approx,
      syncField: field.dataset.syncField || "",
    };
  }

  function syncToFormField(entry) {
    if (!entry.complete || !entry.syncField) return;
    const target = document.getElementById(entry.syncField);
    if (!target) return;
    if (entry.precision === "exact") {
      target.value = entry.iso;
    } else if (!target.value) {
      target.value = entry.iso;
    }
    target.dispatchEvent(new Event("change", { bubbles: true }));
  }

  function getValues(options) {
    const opts = options || {};
    const fields = root.querySelectorAll(".timeline-date-field");
    const entries = [];
    const errors = [];

    fields.forEach((field) => {
      const entry = readField(field);
      if (!entry.complete) return;
      entries.push(entry);
    });

    fields.forEach((field) => {
      const precision = field.querySelector(".timeline-precision")?.value;
      const anyInput =
        field.querySelector(".timeline-date-exact")?.value ||
        field.querySelector(".timeline-month")?.value ||
        field.querySelector(".timeline-year-month")?.value ||
        field.querySelector(".timeline-year-only")?.value;
      const entry = readField(field);

      if (anyInput && !entry.complete) {
        if (precision === "exact") {
          errors.push(entry.label + ": pick a full exact date.");
        } else if (precision === "month") {
          errors.push(entry.label + ": select both month and year.");
        } else {
          errors.push(entry.label + ": select a year.");
        }
      }
    });

    if (opts.requireAll && entries.length < fields.length) {
      const missing = fields.length - entries.length;
      errors.push(
        "Complete all three dates using the dropdowns (" +
          missing +
          " still missing). Use month/year if you are not sure of the exact day."
      );
    }

    return { entries, errors, hasAny: entries.length > 0 };
  }

  function buildStoryLine(entries) {
    const parts = [];
    entries.forEach((e) => {
      if (e.id === "symptom_onset") {
        parts.push("symptoms from " + e.display);
      } else if (e.id === "date_of_absence") {
        parts.push("stopped performing duties " + e.display);
      } else if (e.id === "first_medical_cert") {
        parts.push("first medical certificate " + e.display);
      } else {
        parts.push(e.label.toLowerCase() + " " + e.display);
      }
    });
    return parts.length ? "Timeline: " + parts.join("; ") + "." : "";
  }

  function hydrateFromClaim() {
    root.querySelectorAll(".timeline-date-field").forEach((field) => {
      const syncField = field.dataset.syncField;
      const target = syncField ? document.getElementById(syncField) : null;
      const iso = target?.value || "";
      if (!iso) return;

      const precisionSelect = field.querySelector(".timeline-precision");
      const isFirstOfMonth = iso.endsWith("-01");
      const isJanFirst = iso.endsWith("-01-01");

      if (/^\d{4}-01-01$/.test(iso)) {
        precisionSelect.value = "year";
        field.querySelector(".timeline-year-only").value = iso.slice(0, 4);
      } else if (isFirstOfMonth && !isJanFirst) {
        precisionSelect.value = "month";
        const [y, m] = iso.split("-");
        field.querySelector(".timeline-month").value = m;
        field.querySelector(".timeline-year-month").value = y;
      } else {
        precisionSelect.value = "exact";
        field.querySelector(".timeline-date-exact").value = iso;
      }
      setPickerVisibility(field, precisionSelect.value);
      readField(field);
    });
  }

  function bindField(field) {
    const precisionSelect = field.querySelector(".timeline-precision");
    populateYearSelect(field.querySelector(".timeline-year-month"));
    populateYearSelect(field.querySelector(".timeline-year-only"));

    precisionSelect?.addEventListener("change", () => {
      setPickerVisibility(field, precisionSelect.value);
      readField(field);
    });

    field.querySelectorAll("input, select").forEach((el) => {
      el.addEventListener("change", () => readField(field));
      el.addEventListener("input", () => readField(field));
    });

    setPickerVisibility(field, precisionSelect?.value || "exact");
    readField(field);
  }

  root.querySelectorAll(".timeline-date-field").forEach(bindField);

  if (window.ClaimBuddyTermTips) {
    window.ClaimBuddyTermTips.scan(root);
  }

  hydrateFromClaim();

  window.ClaimBuddyTimeline = {
    getValues,
    buildStoryLine,
    syncToFormField,
    syncAll(entries) {
      (entries || getValues().entries).forEach(syncToFormField);
    },
  };
})();