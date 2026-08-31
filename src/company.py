"""The company page: markup and behaviour for companies.html.

Everything company-facing used to be one band near the bottom of the landing
page, behind four sections addressed to candidates. This is that band given a
page of its own, with the intake moved to the top where a hiring manager who
already knows what they want can act on the first screen.

Chrome, palette and components come from landing.py. Nothing here restyles the
site; it reuses the same tokens and card classes.
"""
from landing import _bars, chip, head_bar, foot, _svg, I

CAL = "https://calendly.com/sathya-goforay/30min"


CSS = """
/* ---- the company page ------------------------------------------------- */
.co-hero{background:linear-gradient(180deg,var(--sky2) 0%,var(--sky3) 45%,var(--bg) 100%);
  padding:clamp(44px,6vw,72px) var(--gut) clamp(40px,5vw,60px)}
.co-hero .wrap{max-width:var(--wrap); margin:0 auto; display:grid; gap:clamp(28px,4vw,56px);
  grid-template-columns:minmax(0,1.05fr) minmax(0,.95fr); align-items:center}
@media(max-width:900px){.co-hero .wrap{grid-template-columns:1fr}}
.co-hero h1{font-size:clamp(34px,5vw,58px); max-width:16ch}
.co-hero .sub{color:var(--muted); font-style:italic; font-size:clamp(14.5px,1.45vw,16px);
  max-width:52ch; margin-top:14px}

/* The intake. Two boxes and a button, sized like something you finish rather
   than something you fill in. */
.co-intake{background:#fff; border:1px solid var(--line); border-radius:20px;
  padding:clamp(20px,2.6vw,28px); box-shadow:0 26px 60px rgba(42,33,64,.14);
  display:flex; flex-direction:column; gap:14px}
.co-intake h2{font-size:19px}
.co-intake textarea,.co-intake input{width:100%; border:1px solid var(--line2); border-radius:12px;
  padding:12px 14px; font:inherit; font-size:14px; background:#fff; color:var(--ink); resize:vertical}
.co-intake textarea{min-height:96px}
.co-intake textarea:focus,.co-intake input:focus{outline:none; border-color:var(--primary)}
.co-intake label{display:block; font-size:11px; font-weight:700; letter-spacing:.14em;
  text-transform:uppercase; color:var(--muted); margin-bottom:6px}
.co-intake .row{display:flex; flex-wrap:wrap; gap:12px; align-items:center}
.co-intake .or{color:var(--muted); font-size:13px}
.co-terms{font-size:12.5px; color:var(--muted); margin:0}
.co-err{color:#B3261E; font-size:13px; min-height:1em; margin:0}
.co-done{display:flex; flex-direction:column; gap:10px; align-items:flex-start}
.co-done .big{font-size:19px; font-weight:600}

.co-strip{max-width:var(--wrap); margin:0 auto; padding:clamp(28px,3.4vw,40px) var(--gut);
  display:flex; flex-wrap:wrap; gap:14px 40px; align-items:center; justify-content:space-between}
.co-strip .n{display:flex; align-items:baseline; gap:9px}
.co-strip .n b{font-size:clamp(22px,2.4vw,30px); letter-spacing:-.03em}
.co-strip ul{display:flex; flex-wrap:wrap; gap:10px; list-style:none}

.co-sec{max-width:var(--wrap); margin:0 auto; padding:clamp(36px,4.6vw,60px) var(--gut)}
.co-sec h2{font-size:clamp(24px,3vw,36px)}
.co-sec .lede{color:var(--muted); max-width:56ch; margin-top:10px}


.co-book{background:var(--tint3); border-top:1px solid var(--line)}
.co-book .wrap{max-width:var(--wrap); margin:0 auto; padding:clamp(36px,4.6vw,60px) var(--gut)}
.co-embed{min-width:320px; height:min(700px,74vh); border-radius:14px; overflow:hidden;
  background:#fff; border:1px solid var(--line); margin-top:20px}
.co-booknote{font-size:12.5px; color:var(--muted); margin-top:10px}
"""

JS = r"""
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
"""


BAND = """    <section class="lp-band">
      <div class="wrap">
        <div class="lp-steps">
          <a href="#book" class="lp-step" style="animation-delay:.05s">
            <span class="lbl">Step 1 &middot; Reach</span>
            <h3>We reach the exact people you want</h3>
            <span class="lp-mini-panel">
              <span style="align-self:flex-start; background:#fff; color:var(--ink); border-radius:10px 10px 10px 3px; padding:6px 10px; font-size:11.5px">
                hey noah, staff platform role at a series B. $210k. interested?</span>
              <span class="lp-out"><span class="av" style="background:var(--primary2); color:#fff">N</span>
                <span class="ln"></span><span class="st">REPLIED</span></span>
              <span class="lp-out"><span class="av" style="background:var(--accent); color:var(--band)">PS</span>
                <span class="ln"></span><span class="st">REPLIED</span></span>
              <span class="lp-out"><span class="av" style="background:var(--band-acc2); color:var(--band)">MT</span>
                <span class="ln"></span><span class="st" style="background:rgba(255,255,255,.12); color:rgba(255,255,255,.75)">REACHED</span></span>
            </span>
            <p>Named lists, message-first. People who ignore InMail answer us.</p>
          </a>

          <a href="#book" class="lp-step" style="animation-delay:.15s">
            <span class="lbl">Step 2 &middot; Introductions</span>
            <h3>Interviews land on your calendar</h3>
            <span class="lp-mini-panel">
              <span class="lp-week">
                <span class="d">MON</span><span class="d">TUE</span><span class="d">WED</span><span class="d">THU</span><span class="d">FRI</span>
                <span class="c"></span>
                <span class="c" style="background:var(--primary2); color:#fff">N 2:30</span>
                <span class="c"></span>
                <span class="c" style="background:var(--accent); color:var(--band)">PS 11:00</span>
                <span class="c" style="background:var(--band-acc2); color:var(--band)">MT 4:00</span>
              </span>
            </span>
            <p>Five per role, pre-interviewed, with our read attached.</p>
          </a>

          <a href="#book" class="lp-step" style="animation-delay:.25s">
            <span class="lbl">Step 3 &middot; Success fee</span>
            <h3>We earn when you hire</h3>
            <span class="lp-mini-panel lp-ledger">
              <div class="win"><span class="tick">{icon_check_dark}</span>
                <span style="font-weight:600">Offer signed</span>
                <span class="amt" style="color:var(--band-acc)">success fee</span></div>
              <div>{icon_x_m}<span style="color:rgba(255,255,255,.75)">No hire</span><span class="amt" style="color:rgba(255,255,255,.75)">$0</span></div>
              <div>{icon_x_m}<span style="color:rgba(255,255,255,.75)">Retainers</span><span class="amt" style="color:rgba(255,255,255,.75)">never</span></div>
            </span>
            <p>We make money when you make money.</p>
          </a>
        </div>

        <div class="lp-funnel">
          <div class="lp-funnel-top lbl"><span>Everyone who could do the job</span>
            <span class="hit">Five reach your calendar</span></div>
          <div class="lp-bars" aria-hidden="true">{bars}</div>
          <div class="lp-funnel-foot"><span>1,500 profiles reviewed per search</span>
            <span aria-hidden="true">&rarr;</span>
            <span style="color:var(--band-acc)">5 introductions, with our read on each</span></div>
        </div>

      </div>
    </section>
"""


def body():
    """The company page, from the ticker down to the footer."""
    band = BAND.format(
        bars=_bars(),
        icon_check_dark=_svg(I["check"], 12, "var(--band)", extra=' stroke-width="3"'),
        icon_x_m=_svg(I["x"], 14, "rgba(255,255,255,.5)"),
    )
    chips = "".join([
        chip("anthropic", "Anthropic", "0"),
        chip("openai", "OpenAI", ".2"),
        chip("googlegemini", "Google DeepMind", ".4"),
        chip("meta", "Meta", ".6"),
        chip("stripe", "Stripe", ".8"),
    ])
    return ("""
<div class="lp">

""" + head_bar("companies") + """
  <main>
    <section class="co-hero">
      <div class="wrap">
        <div>
          <span class="lbl" style="color:var(--primary)">For companies</span>
          <h1>Five candidates on your calendar. You pay when you hire.</h1>
          <p class="sub">Send us any role and consider it handled. We reach the people you
            want, interview every one ourselves, and hand you introductions with our read
            attached.</p>
        </div>

        <form class="co-intake" id="co-form" novalidate>
          <h2 id="role">Send us a role.</h2>
          <div>
            <label for="co-jd">The role</label>
            <textarea id="co-jd" name="jd" maxlength="20000"
                      placeholder="Paste a job link, or the description itself."></textarea>
          </div>
          <div>
            <label for="co-email">Where we reply</label>
            <input id="co-email" name="email" type="email" autocomplete="email"
                   maxlength="320" placeholder="you@company.com">
          </div>
          <!-- bots fill every field they find; people never see this one -->
          <input type="text" name="confirm_url" tabindex="-1" autocomplete="off"
                 aria-hidden="true" style="position:absolute; left:-9999px; width:1px; height:1px">
          <p class="co-err" id="co-err" role="alert"></p>
          <p class="co-terms">No retainer. You pay only when you hire.</p>
          <div class="row">
            <button type="submit" class="lp-btn" id="co-submit">Send it over</button>
            <span class="or">or <a href="#book" style="color:var(--primary); text-decoration:underline;
              text-underline-offset:2px">book 15 minutes</a></span>
          </div>
        </form>

        <div class="co-intake co-done" id="co-done" hidden>
          <span class="big">On it.</span>
          <p style="color:var(--muted)">We start on the search today and come back to you within
            a day, with names and our read on each. Nothing is owed unless you hire.</p>
          <a class="lp-btn" href="#book">Book 15 minutes</a>
        </div>
      </div>
    </section>

    <div class="co-strip">
      <div class="n"><b>1,500+</b><span class="lbl" style="color:var(--muted)">candidates
        pre-interviewed</span></div>
      <div class="n"><b>$0</b><span class="lbl" style="color:var(--muted)">until you hire</span></div>
      <ul>{chips}</ul>
    </div>

{band}

    <section class="co-book" id="book">
      <div class="wrap">
        <h2>Grab 15 minutes.</h2>
        <p class="lede">Bring the role. We will walk you through the pool and show you what our
          read looks like.</p>
        <div class="co-embed calendly-inline-widget" id="co-embed" data-url="{cal}"></div>
        <p class="co-booknote">Not loading? <a href="{cal}" target="_blank" rel="noopener">Open the
          calendar in a new tab</a>.</p>
      </div>
    </section>

    <section class="lp-crosslink">
      <div class="wrap">
        <a href="index.html">
          <span><b>Looking for a role yourself?</b> Foray finds them, writes the application,
            and applies for you.</span>
          <span class="go" aria-hidden="true">&rarr;</span>
        </a>
      </div>
    </section>
  </main>

""" + foot("companies") + """
</div>
""").replace("{band}", band).replace("{chips}", chips) \
     .replace("{cal}", CAL)
