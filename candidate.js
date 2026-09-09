(function () {
  var form = document.getElementById("ca-form");
  if (!form) return;

  var err = document.getElementById("ca-err");
  var done = document.getElementById("ca-done");
  var btn = document.getElementById("ca-submit");

  /* Mirrors FORMS.engineer in api/submit.js. GitHub, phone and location are
     collected but not required -- see the note there. */
  var REQUIRED = ["Name", "Email", "LinkedIn", "What they want next"];
  var OPTIONAL = ["Phone", "GitHub", "Location"];
  var EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (btn.disabled) return;

    var fields = {};
    var firstBad = null;

    REQUIRED.concat(OPTIONAL).forEach(function (key) {
      var box = form.elements[key];
      if (!box) return;
      var val = (box.value || "").trim();
      if (val) fields[key] = val;

      var required = REQUIRED.indexOf(key) > -1;
      /* The browser's own checks run first; this is only so the first bad box
         gets focus rather than the whole form getting one blanket error. */
      var bad = (required && !val) || (key === "Email" && val && !EMAIL.test(val));
      box.setAttribute("aria-invalid", bad ? "true" : "false");
      if (bad && !firstBad) firstBad = box;
    });

    if (firstBad) {
      err.textContent = "Please check the highlighted field.";
      firstBad.focus();
      return;
    }

    err.textContent = "";
    btn.disabled = true;
    btn.textContent = "Sending…";
    var slow = setTimeout(function () {
      if (btn.disabled) btn.textContent = "Still going…";
    }, 4000);

    fetch("/api/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        kind: "engineer",
        fields: fields,
        confirm_url: (form.elements.confirm_url || {}).value || ""
      })
    }).then(function (r) {
      return r.json().catch(function () { return { ok: false }; });
    }).then(function (out) {
      clearTimeout(slow);
      if (!out || !out.ok) throw new Error((out && out.error) || "That did not go through.");
      form.hidden = true;
      done.hidden = false;
      done.scrollIntoView({ behavior: "smooth", block: "center" });
    }).catch(function (e2) {
      clearTimeout(slow);
      btn.disabled = false;
      btn.textContent = "Send it over";
      err.textContent = e2.message || "That did not go through. Try again in a moment.";
    });
  });
})();