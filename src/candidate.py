"""The candidate page: markup and behaviour for candidates.html.

Not the old landing page. That one is parked in src/parked/candidates.py and
sold an autonomous agent; this is a recruiting agency asking an engineer to
introduce themselves so we have them on file when a search fits.

It exists for two reasons, in this order:

  1. It builds the roster. Every submission is a row we can search when a
     client brief lands, which is the whole point of collecting them.
  2. It is where somebody we have reached out to ends up when they look us up.
     That is why the hero says plainly that we do outreach and that a person
     will reply. A candidate arriving here should conclude "small search firm
     in San Francisco", not "I was messaged by software".

Copy rule, same as the homepage: no agent, no automation, nothing that reads as
a product. Promises here are service promises a human can keep -- we reply, we
name the company, we tell you the comp. Do not add a claim this page cannot
honour, because the people reading it have already been contacted by us.

Chrome, palette and the form components come from landing.py and company.py
(``co-hero``, ``co-intake``); this adds only what is specific to the page.
"""
from landing import head_bar, foot, _svg, I

CSS = """
/* ---- the candidate page ------------------------------------------------ */
.ca-note{display:flex; gap:10px; align-items:flex-start; margin-top:18px; padding:12px 14px;
  background:#fff; border:1px solid var(--line); border-radius:12px; max-width:46ch}
.ca-note svg{flex:none; margin-top:1px}
.ca-note p{font-size:13px; color:var(--muted); margin:0}
.ca-note b{color:var(--ink); font-weight:600}

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
    icon_info = _svg(I["eye"], 16, "var(--primary)")
    fields = (
        _field("Name", "Your name", auto="name", ph="Priya Sharma")
        + _field("Email", "Email", kind="email", auto="email", ph="you@gmail.com")
        + _field("LinkedIn", "LinkedIn", kind="url", auto="url",
                 ph="linkedin.com/in/…")
        + _field("Phone", "Phone", kind="tel", auto="tel", ph="For a quick call",
                 required=False)
        + _field("GitHub", "GitHub", kind="url", ph="github.com/…",
                 required=False)
        + _field("Location", "Where you are", ph="San Francisco, or remote",
                 required=False)
        + _field("What they want next", "What you want next", wide=True, rows=True,
                 ph="The kind of engineering you want to be doing, the stage of company, "
                    "and the comp you are targeting. A couple of lines is plenty.")
    )

    return ("""
<div class="lp">

""" + head_bar("candidates") + """
  <main>
    <section class="co-hero">
      <div class="wrap">
        <div>
          <span class="lbl" style="color:var(--primary)">For engineers</span>
          <h1>Tell us what you want next.</h1>
          <p class="sub">Foray is a recruiting agency in San Francisco. We run engineering
            searches for startups from seed through growth stage, which means we spend our
            days talking to the companies doing the hiring. Introduce yourself and we will
            come to you when one of those searches is a genuine fit.</p>

          <div class="ca-note">
            """ + icon_info + """
            <p><b>Did we reach out to you?</b> That was us, and a person here is on the
              other end of it. If you would rather we did not contact you again, say so in
              any reply and we will stop.</p>
          </div>
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
          <p style="color:var(--muted)">We read every one of these. If something we are
            working lines up with what you described, you will hear from a person here with
            the company named and the comp up front. If nothing fits yet, we will hold onto
            your details rather than pretend otherwise.</p>
        </div>
      </div>
    </section>

    <section class="ca-work" id="work">
      <div class="wrap">
        <h2>How we work with you.</h2>
        <p class="lede" style="color:var(--muted); max-width:56ch; margin-top:10px">Recruiters
          have earned their reputation. These are the things we do differently, and you can
          hold us to all three.</p>

        <div class="ca-cards">
          <div class="ca-card">
            <span class="ic">""" + _svg(I["check"], 18, "var(--primary)") + """</span>
            <h3>We name the company</h3>
            <p>No blind pitches about &ldquo;a well-funded startup&rdquo;. You get the
              company, the role and the team before you decide whether you are interested.</p>
          </div>
          <div class="ca-card">
            <span class="ic">""" + _svg(I["check"], 18, "var(--primary)") + """</span>
            <h3>Comp up front</h3>
            <p>We tell you the range at the start, not after two interviews. If it is below
              what you told us you wanted, we will not waste your afternoon.</p>
          </div>
          <div class="ca-card">
            <span class="ic">""" + _svg(I["check"], 18, "var(--primary)") + """</span>
            <h3>You never chase us</h3>
            <p>We chase the client for feedback and pass it on either way, including a no.
              Silence is the thing engineers hate most about recruiters and it is the easiest
              to fix.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="lp-crosslink">
      <div class="wrap">
        <a href="index.html">
          <span><b>Hiring engineers?</b> Send us the role and we will bring you five
            candidates worth interviewing.</span>
          <span class="go" aria-hidden="true">&rarr;</span>
        </a>
      </div>
    </section>
  </main>

""" + foot("candidates") + """
</div>
""")
