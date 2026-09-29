(function () {
  const form = document.getElementById("policy-reader-upload");
  if (!form) return;

  form.addEventListener("submit", () => {
    const btn = form.querySelector('button[type="submit"]');
    if (btn) {
      btn.disabled = true;
      btn.textContent = "Scanning policy…";
    }
  });
})();