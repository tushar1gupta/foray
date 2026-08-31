(function () {
  var root = document.querySelector(".lp");
  if (!root) return;

  /* the clock is gone from the bar, but keep the guard shape landing.js uses */
  var form = document.getElementById("co-form");
  if (form) {
    var err = document.getElementById("co-err");
    var done = document.getElementById("co-done");
    var btn = document.getElementById("co-submit");
    var jd = form.elements.jd;
    var email = form.elements.email;

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (btn.disabled) return;

      var jdVal = (jd.value || "").trim();
      var mailVal = (email.value || "").trim();
      if (!jdVal) {
        err.textContent = "Paste the link or the description and we'll take it from there.";
        jd.focus();
        return;
      }
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(mailVal)) {
        err.textContent = "We need an address to send the shortlist to.";
        email.focus();
        return;
      }

      /* One box takes either a link or the description itself, so nobody has to
         pick which they have. Which field it lands in is decided here. */
      var fields = { Email: mailVal };
      if (/^https?:\/\//i.test(jdVal)) fields["Job posting link"] = jdVal;
      else fields["Job description"] = jdVal;

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
          kind: "company",
          fields: fields,
          confirm_url: (form.elements.confirm_url || {}).value || ""
        })
      }).then(function (r) {
        return r.json().catch(function () { return { ok: false }; });
      }).then(function (out) {
        clearTimeout(slow);
        if (!out || !out.ok) throw new Error((out && out.error) || "That did not go through.");
        btn.disabled = false;
        btn.textContent = "Send it over";
        form.hidden = true;
        done.hidden = false;
      }).catch(function (e2) {
        clearTimeout(slow);
        btn.disabled = false;
        btn.textContent = "Send it over";
        err.textContent = e2.message || "That did not go through. Try again in a moment.";
      });
    });
  }

  /* Calendly is a third party and the embed is below the fold, so it is fetched
     when the booking section first comes into view rather than on load. */
  var slot = document.getElementById("co-embed");
  if (slot) {
    var asked = false;
    function load() {
      if (asked) return;
      asked = true;
      var sc = document.createElement("script");
      sc.src = "https://assets.calendly.com/assets/external/widget.js";
      sc.async = true;
      document.head.appendChild(sc);
    }
    if (window.IntersectionObserver) {
      var io = new IntersectionObserver(function (es) {
        if (es.some(function (x) { return x.isIntersecting; })) { load(); io.disconnect(); }
      }, { rootMargin: "400px" });
      io.observe(slot);
    } else {
      load();
    }
  }
})();