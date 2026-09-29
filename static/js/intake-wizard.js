/** Stepped intake — one section per screen, Next / Previous navigation. */
(function () {
  const form = document.querySelector(".intake-wizard-form");
  if (!form) return;

  const INTAKE_STEPS = 8;
  const SECTION_BY_ID = {
    "section-policy": 0,
    "section-claim-stage": 1,
    "section-parties": 2,
    "section-occupation": 3,
    "section-health-story": 4,
    "section-salary": 5,
    "section-dates": 6,
    "section-notes": 7,
  };

  const COACHING = [
    "Start with the cover you actually have. Upload the policy, schedule, member certificate or employer benefits booklet if available — you can correct extracted details later.",
    "Choose the stage that best describes today. This changes the evidence gaps, deadlines and next actions ClaimBuddy prioritises.",
    "Capture the people and references around the claim: employer, insurer, policyholder, policy number and claim reference. Leave anything unknown blank.",
    "Describe the job as real material duties, not only a title. ClaimBuddy uses this later when mapping functional limitations to the policy test.",
    "Build the health story around function: what changed, when it changed, and what you can no longer do reliably or repeatedly.",
    "Capture the earnings and deductions relevant to the benefit calculation, or add payslips so the record can be completed later.",
    "Keep each important date separate — symptom onset, Date of Absence, first certificate, first notice, submission and decision dates may all differ.",
    "Add record-access status or context that belongs in the file but not in another section. Then create the workspace and refine it module by module.",
  ];

  const stepTabs = form.querySelectorAll(".intake-step-tab");
  const screens = form.querySelectorAll(".intake-screen");
  const prevBtn = document.getElementById("intake-step-prev");
  const nextBtn = document.getElementById("intake-step-next");
  const submitBtn = document.getElementById("intake-step-submit");
  const coach = document.getElementById("intake-coach");
  const claimStage = document.getElementById("claim_stage");

  let activeStep = 0;

  function updateCoach(step) {
    if (!coach) return;
    const msg = COACHING[step] || "";
    coach.textContent = msg;
    coach.hidden = !msg;
  }

  function setIntakeStep(index, opts) {
    const options = opts || {};
    activeStep = Math.max(0, Math.min(INTAKE_STEPS - 1, index));

    stepTabs.forEach((tab) => {
      const step = Number(tab.dataset.intakeStep);
      tab.classList.toggle("is-active", step === activeStep);
      tab.classList.toggle("is-complete", step < activeStep);
    });

    screens.forEach((screen) => {
      const show = Number(screen.dataset.intakeStep) === activeStep;
      screen.hidden = !show;
      screen.classList.toggle("is-active", show);
    });

    if (prevBtn) prevBtn.disabled = activeStep === 0;
    if (nextBtn) nextBtn.hidden = activeStep === INTAKE_STEPS - 1;
    if (submitBtn) submitBtn.hidden = activeStep !== INTAKE_STEPS - 1;

    updateCoach(activeStep);

    if (options.focusFieldId) {
      const el = document.getElementById(options.focusFieldId);
      if (el) {
        window.requestAnimationFrame(() => {
          el.scrollIntoView({ behavior: "smooth", block: "center" });
          el.focus({ preventScroll: true });
        });
      }
    } else if (!options.silent) {
      const activeScreen = form.querySelector('.intake-screen[data-intake-step="' + activeStep + '"]');
      if (activeScreen) activeScreen.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }

  function policyStepReady() {
    if (typeof window.policyPlanState === "function") {
      return window.policyPlanState().ready;
    }
    var planInput = document.getElementById("policy_plan_type");
    return !!(planInput && planInput.value);
  }

  function canAdvanceFrom(step) {
    if (step === 0 && !policyStepReady()) {
      return false;
    }
    if (step === 1 && claimStage && !claimStage.value) {
      return false;
    }
    return true;
  }

  function goToSectionId(sectionId, focusFieldId) {
    const step = SECTION_BY_ID[sectionId];
    if (step === undefined) return;
    setIntakeStep(step, { focusFieldId: focusFieldId || null });
  }

  stepTabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      setIntakeStep(Number(tab.dataset.intakeStep));
    });
  });

  prevBtn?.addEventListener("click", () => setIntakeStep(activeStep - 1));
  nextBtn?.addEventListener("click", () => {
    if (!canAdvanceFrom(activeStep)) {
      if (coach) {
        if (activeStep === 0) {
          var state =
            typeof window.policyPlanState === "function"
              ? window.policyPlanState()
              : {};
          if (!state.planType) {
            coach.textContent =
              "Choose whether this is a group or private plan before continuing.";
          } else {
            coach.textContent =
              "Select your insurer (or enter the name under Other) before continuing.";
          }
        } else {
          coach.textContent = "Please select your claim stage before continuing.";
        }
        coach.hidden = false;
      }
      if (activeStep === 0) {
        var picker = document.getElementById("policy-plan-picker");
        if (picker && !picker.hidden) picker.scrollIntoView({ behavior: "smooth", block: "center" });
        else document.getElementById("policy-private-flow")?.scrollIntoView({ behavior: "smooth", block: "center" });
      } else if (activeStep === 1) {
        document.getElementById("claim-stage-picker")?.scrollIntoView({ behavior: "smooth", block: "center" });
      } else {
        claimStage?.focus();
      }
      return;
    }
    setIntakeStep(activeStep + 1);
  });

  form.addEventListener("click", (e) => {
    const link = e.target.closest('a[href^="#section-"]');
    if (!link || !form.contains(link)) return;
    const id = (link.getAttribute("href") || "").slice(1);
    if (SECTION_BY_ID[id] === undefined) return;
    e.preventDefault();
    goToSectionId(id);
  });

  document.addEventListener("claimbuddy:intake-goto", (e) => {
    const detail = e.detail || {};
    if (detail.sectionId) goToSectionId(detail.sectionId, detail.focusFieldId);
    else if (typeof detail.step === "number") {
      setIntakeStep(detail.step, { focusFieldId: detail.focusFieldId || null });
    }
  });

  function goToStep(step, focusFieldId) {
    setIntakeStep(step, { focusFieldId: focusFieldId || null });
  }

  window.ClaimBuddyIntake = { goToSectionId, goToStep, get activeStep() { return activeStep; } };

  const hash = (window.location.hash || "").slice(1);
  if (SECTION_BY_ID[hash] !== undefined) {
    setIntakeStep(SECTION_BY_ID[hash], { silent: true });
  } else {
    setIntakeStep(0, { silent: true });
  }
})();