(function () {
  var drop = document.getElementById("compiler-drop");
  var input = document.getElementById("compiler-files");
  if (!drop || !input) return;

  ["dragenter", "dragover"].forEach(function (evt) {
    drop.addEventListener(evt, function (e) {
      e.preventDefault();
      e.stopPropagation();
      drop.classList.add("is-dragover");
    });
  });
  ["dragleave", "drop"].forEach(function (evt) {
    drop.addEventListener(evt, function (e) {
      e.preventDefault();
      e.stopPropagation();
      drop.classList.remove("is-dragover");
    });
  });
  drop.addEventListener("drop", function (e) {
    var files = e.dataTransfer && e.dataTransfer.files;
    if (!files || !files.length) return;
    input.files = files;
    var form = drop.closest("form");
    if (form) form.submit();
  });
})();
