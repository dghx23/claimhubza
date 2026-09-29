/** Rejection explainer — upload form UX. */
(function () {
  const form = document.getElementById("rejection-explainer-upload");
  const fileInput = document.getElementById("rejection-file");
  if (!form || !fileInput) return;

  form.addEventListener("submit", () => {
    const btn = form.querySelector('button[type="submit"]');
    if (btn) {
      btn.disabled = true;
      btn.textContent = "Uploading & scanning…";
    }
  });
})();