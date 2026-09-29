(() => {
  const key = "claimhub-resources-theme";
  const root = document.documentElement;
  const buttons = () => document.querySelectorAll("[data-chr-theme-toggle]");

  function preferred() {
    const saved = localStorage.getItem(key);
    if (saved === "dark" || saved === "light") return saved;
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }

  function apply(theme, persist=false) {
    root.setAttribute("data-chr-theme", theme);
    root.style.colorScheme = theme;
    buttons().forEach(btn => {
      const dark = theme === "dark";
      btn.setAttribute("aria-pressed", dark ? "true" : "false");
      btn.setAttribute("aria-label", dark ? "Switch to light mode" : "Switch to dark mode");
      const icon = btn.querySelector("[data-theme-icon]");
      const label = btn.querySelector("[data-theme-label]");
      if (icon) icon.textContent = dark ? "☀" : "☾";
      if (label) label.textContent = dark ? "Light" : "Dark";
    });
    if (persist) localStorage.setItem(key, theme);
  }

  apply(preferred());

  document.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-chr-theme-toggle]");
    if (!btn) return;
    apply(root.getAttribute("data-chr-theme") === "dark" ? "light" : "dark", true);
  });

  document.addEventListener("DOMContentLoaded", () => apply(root.getAttribute("data-chr-theme") || preferred()));
})();