"""The candidate page: markup and behaviour for candidates.html.

Not the old landing page. That one is parked in src/parked/candidates.py and
sold an autonomous agent; this is a recruiting agency asking someone to
introduce themselves so we have them on file when a search fits.

It exists for two reasons, in this order:

  1. It builds the roster. Every submission is a row we can search when a
     client brief lands, which is the whole point of collecting them.
  2. It is where somebody we have reached out to ends up when they look us up.
     A candidate arriving here should conclude "small search firm in San
     Francisco", not "I was messaged by software". It does this by reading like
     a firm, not by discussing the outreach: a note acknowledging that we
     contacted them was tried and removed. Raising it on the page draws
     attention to the cold contact and invites the question of how they were
     found, which is a conversation for a reply, not a landing page.

Copy rules, same as the homepage: no agent, no automation, nothing that reads as
a product, and no function named -- we may search for any of them, and this page
is read by people we cold-messaged who have not told us their discipline yet.

Third rule, and the reason this page has no "how we work with you" section:
**it promises nothing.** It once carried three service pledges -- we name the
company, comp up front, you never chase us -- and they were cut deliberately.
Every one of them is a commitment that breaks first under volume, on a page read
by people we contacted, which is the worst place to be caught out. State facts
about the firm instead: who pays us, what stage of company we work with, what
happens to a submission. If you are tempted to add a service level here, put it
in the outreach where a person can actually stand behind it.

Chrome, palette and the form components come from landing.py and company.py
(``co-hero``, ``co-intake``); this adds only what is specific to the page.
"""
from landing import head_bar, foot, _svg, I

CSS = """
/* ---- the candidate page ------------------------------------------------ */
.ca-work{background:var(--tint3); border-top:1px solid var(--line);
  border-bottom:1px solid var(--line)}
.ca-work .wrap{max-width:var(--wrap); margin:0 auto;
  padding:clamp(36px,4.6vw,60px) var(--gut)}
.ca-cards{display:grid; gap:16px; margin-top:24px;
  grid-template-columns:repeat(3,minmax(0,1fr))}
@media(max-width:860px){.ca-cards{grid-template-columns:1fr}}
.ca-card{background:#fff; border:1px solid var(--line); border-radius:16px;
  padding:clamp(18px,2.2vw,24px); display:flex; flex-direction:column; gap:9px}
.ca-card h3{font-size:16.5px}
.ca-card p{font-size:13.5px; color:var(--muted); margin:0}
.ca-card .ic{width:34px; height:34px; border-radius:9px; background:var(--tint2);
  display:grid; place-items:center; margin-bottom:3px}

.ca-fields{display:grid; gap:14px; grid-template-columns:1fr 1fr}
.ca-fields .wide{grid-column:1 / -1}
@media(max-width:560px){.ca-fields{grid-template-columns:1fr}}
.ca-opt{font-weight:400; letter-spacing:0; text-transform:none; color:var(--muted);
  font-size:11px}
"""

JS = r"""
(function () {
  var form = document.getElementById("ca-form");
  if (!form) return;

  var err = document.getElementById("ca-err");
  var done = document.getElementById("ca-done");
  var btn = document.getElementById("ca-submit");

  /* Mirrors FORMS.candidate in api/submit.js. Portfolio, phone and location are
     collected but not required -- see the note there. */
  var REQUIRED = ["Name", "Email", "LinkedIn", "What they want next"];
  var OPTIONAL = ["Phone", "Portfolio", "Location"];
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
        kind: "candidate",
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
"""


def _field(key, label, kind="text", auto=None, ph="", wide=False, required=True,
           rows=False):
    """One labelled box. Optional boxes say so, because an unmarked empty field
    reads as an obstacle on a form nobody is obliged to fill in."""
    fid = "ca-" + key.lower().replace(" ", "-")
    cls = ' class="wide"' if wide else ""
    opt = "" if required else ' <span class="ca-opt">optional</span>'
    req = " required" if required else ""
    auto = ' autocomplete="%s"' % auto if auto else ""
    if rows:
        box = ('<textarea id="%s" name="%s" maxlength="8000" placeholder="%s"%s></textarea>'
               % (fid, key, ph, req))
    else:
        box = ('<input id="%s" name="%s" type="%s" maxlength="320" placeholder="%s"%s%s>'
               % (fid, key, kind, ph, auto, req))
    return ('          <div%s>\n'
            '            <label for="%s">%s%s</label>\n'
            '            %s\n'
            '          </div>\n' % (cls, fid, label, opt, box))


def body():
    """The candidate page, from the ticker down to the footer."""
    fields = (
        _field("Name", "Your name", auto="name", ph="Priya Sharma")
        + _field("Email", "Email", kind="email", auto="email", ph="you@gmail.com")
        + _field("LinkedIn", "LinkedIn", kind="url", auto="url",
                 ph="linkedin.com/in/…")
        + _field("Phone", "Phone", kind="tel", auto="tel", ph="For a quick call",
                 required=False)
        + _field("Portfolio", "Portfolio or GitHub", kind="url",
                 ph="A site, a repo, anything you would show", required=False)
        + _field("Location", "Where you are", ph="San Francisco, or remote",
                 required=False)
        + _field("What they want next", "What you want next", wide=True, rows=True,
                 ph="The kind of work you want to be doing, the stage of company, and the "
                    "comp you are targeting. A couple of lines is plenty.")
    )

    return ("""
<div class="lp">

""" + head_bar("candidates") + """
  <main>
    <section class="co-hero">
      <div class="wrap">
        <div>
          <span class="lbl" style="color:var(--primary)">For candidates</span>
          <h1>Tell us what you want next.</h1>
          <p class="sub">Foray is a recruiting agency in San Francisco. We run searches for
            startups from seed through growth stage, which means we spend our days talking to
            the companies doing the hiring. Introduce yourself and we will keep you in mind
            for the searches we run.</p>
        </div>

        <form class="co-intake" id="ca-form" novalidate>
          <h2 id="intro">Introduce yourself.</h2>
          <div class="ca-fields">
""" + fields + """          </div>
          <!-- bots fill every field they find; people never see this one -->
          <input type="text" name="confirm_url" tabindex="-1" autocomplete="off"
                 aria-hidden="true" style="position:absolute; left:-9999px; width:1px; height:1px">
          <p class="co-err" id="ca-err" role="alert"></p>
          <p class="co-terms">Free for you, always. Companies pay us when they hire. See how
            we handle your details in our <a href="privacy.html" style="color:var(--primary);
            text-decoration:underline; text-underline-offset:2px">privacy policy</a>.</p>
          <button type="submit" class="lp-btn" id="ca-submit">Send it over</button>
        </form>

        <div class="co-intake co-done" id="ca-done" hidden>
          <span class="big">Thanks &mdash; you are on our list.</span>
          <p style="color:var(--muted)">Your details are with us now. We get in touch when a
            client brief looks like what you described, which means it depends on what they
            are hiring for rather than on anything we can put a date on.</p>
        </div>
      </div>
    </section>

    <section class="ca-work" id="work">
      <div class="wrap">
        <h2>How this works.</h2>
        <p class="lede" style="color:var(--muted); max-width:56ch; margin-top:10px">Three
          things worth knowing before you send anything, so you can judge whether it is
          worth your time.</p>

        <div class="ca-cards">
          <div class="ca-card">
            <span class="ic">""" + _svg(I["check"], 18, "var(--primary)") + """</span>
            <h3>The companies pay us</h3>
            <p>A client pays us a fee when they hire someone we introduced. That is the
              entire business model, and it is why there is no charge to you at any point.</p>
          </div>
          <div class="ca-card">
            <span class="ic">""" + _svg(I["check"], 18, "var(--primary)") + """</span>
            <h3>Startups, seed to growth</h3>
            <p>That is the range we run searches across, in every function a company of
              that size hires for. If you are aiming somewhere else, we are probably not
              much use to you.</p>
          </div>
          <div class="ca-card">
            <span class="ic">""" + _svg(I["check"], 18, "var(--primary)") + """</span>
            <h3>You go on the list</h3>
            <p>What you send sits with us. When a brief comes in that looks like what you
              described, that is the point at which you hear from us &mdash; so it depends
              on what our clients are hiring for.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="lp-crosslink">
      <div class="wrap">
        <a href="index.html">
          <span><b>Hiring?</b> Send us the role and we will bring you five candidates
            worth interviewing.</span>
          <span class="go" aria-hidden="true">&rarr;</span>
        </a>
      </div>
    </section>
  </main>

""" + foot("candidates") + """
</div>
""")
