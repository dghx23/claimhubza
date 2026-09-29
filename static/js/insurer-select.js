/** NFO life insurer select with "Other" free-text fallback. */
(function () {
  "use strict";

  var select = document.getElementById("insurer");
  var otherWrap = document.getElementById("insurer-other-wrap");
  var otherInput = document.getElementById("insurer_other");
  if (!select) return;

  function toggleOther() {
    var isOther = select.value === "__other__";
    if (otherWrap) otherWrap.hidden = !isOther;
    if (isOther && otherInput) {
      window.requestAnimationFrame(function () {
        otherInput.focus();
      });
    }
  }

  select.addEventListener("change", function () {
    toggleOther();
    select.dispatchEvent(new Event("change", { bubbles: true }));
  });

  toggleOther();

  window.setInsurerSelectValue = function (name) {
    if (!name) return false;
    var options = Array.prototype.slice.call(select.options);
    var match = options.find(function (opt) {
      return opt.value && opt.value !== "__other__" && opt.value === name;
    });
    if (match) {
      select.value = match.value;
      toggleOther();
      return true;
    }
    select.value = "__other__";
    if (otherInput) otherInput.value = name;
    toggleOther();
    return false;
  };
})();