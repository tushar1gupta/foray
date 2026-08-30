(function () {
  "use strict";
  var lp = document.querySelector(".lp");
  if (!lp) return;

  /* San Francisco clock in the header. */
  var clock = document.getElementById("lp-clk");
  function tick() {
    if (!clock) return;
    clock.textContent = new Intl.DateTimeFormat("en-US", {
      timeZone: "America/Los_Angeles", hour: "2-digit", minute: "2-digit", hour12: false
    }).format(new Date());
  }
  tick();
  setInterval(tick, 30000);

  /* ---- dialogs -------------------------------------------------------- */
  var clip = document.getElementById("lp-voice");
  /* Calendly's widget is a third party, and most visitors never open the hire
     dialog. Fetch it the first time somebody does rather than on every page
     load. widget.js scans for .calendly-inline-widget when it runs, and by then
     the container is already in the document. */
  var calendarAsked = false;
  function loadCalendar() {
    if (calendarAsked) return;
    calendarAsked = true;
    var s = document.createElement("script");
    s.src = "https://assets.calendly.com/assets/external/widget.js";
    s.async = true;
    document.head.appendChild(s);
  }

  function playVoice() {
    if (!clip) return;
    try {
      clip.currentTime = 0;
      var p = clip.play();
      if (p && p.catch) p.catch(function () {});
    } catch (err) { /* autoplay refused: the Hear button still works */ }
  }
  function stopVoice() {
    if (!clip) return;
    try { clip.pause(); clip.currentTime = 0; } catch (err) {}
  }

  document.addEventListener("click", function (e) {
    /* Puts the visitor back at the top, where the waitlist and the agent both
       are, and opens the form once the scroll has settled. Opening it mid-flight
       parks the page somewhere odd behind the dialog. */
    if (e.target.closest("[data-waitlist]")) {
      var from = e.target.closest("dialog");
      if (from) from.close();
      /* Instant, not smooth. Opening the dialog locks the page, and a smooth
         scroll still running at that moment stops dead -- from the foot of the
         page that leaves the visitor exactly where they started. The dialog
         covers the jump, and what matters is where they land when they close
         it. */
      var hero = document.getElementById("lp-hero");
      if (hero) window.scrollTo({ top: hero.offsetTop, behavior: "instant" });
      requestAnimationFrame(function () {
        var wl = document.getElementById("lp-waitlist");
        if (wl && wl.showModal && !wl.open) wl.showModal();
      });
      return;
    }

    var open = e.target.closest("[data-open]");
    if (open) {
      var d = document.getElementById(open.getAttribute("data-open"));
      if (d && d.showModal) {
        d.showModal();
        if (d.id === "lp-call") playVoice();
        if (d.id === "lp-hire") loadCalendar();
      }
      return;
    }
    if (e.target.closest("[data-close]")) {
      var host = e.target.closest("dialog");
      if (host) host.close();
      return;
    }
    if (e.target.closest("[data-hear]")) { playVoice(); return; }
    if (e.target.closest("[data-chat]")) {
      var host2 = e.target.closest("dialog");
      if (host2) host2.close();
      var card = document.getElementById("lp-phone");
      if (card && card.scrollIntoView) card.scrollIntoView({ behavior: "smooth", block: "center" });
      var box = document.getElementById("lp-input");
      if (box) setTimeout(function () { box.focus(); }, 400);
    }
  });

  Array.prototype.forEach.call(document.querySelectorAll("dialog"), function (d) {
    /* clicking the backdrop closes; the inner box stops the bubble */
    d.addEventListener("click", function (e) { if (e.target === d) d.close(); });
    d.addEventListener("close", stopVoice);
  });


  /* ---- waitlist ------------------------------------------------------- */
  var wlForm = document.getElementById("lp-wl-form");
  if (wlForm) {
    var wlErr = document.getElementById("lp-wl-err");
    var wlDone = document.getElementById("lp-wl-done");
    var wlSubmit = document.getElementById("lp-wl-submit");

    wlForm.addEventListener("submit", function (e) {
      e.preventDefault();
      if (wlSubmit.disabled) return;

      var fields = {};
      var firstBad = null;
      ["Name", "Email", "Phone"].forEach(function (key) {
        var box = wlForm.elements[key];
        var val = (box.value || "").trim();
        fields[key] = val;
        // The browser's own required/type checks are the first pass; this is
        // only so the first empty box gets focus rather than a blanket error.
        var bad = !val || (key === "Email" && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(val));
        box.setAttribute("aria-invalid", bad ? "true" : "false");
        if (bad && !firstBad) firstBad = box;
      });
      if (firstBad) {
        wlErr.textContent = "Please check the highlighted field.";
        firstBad.focus();
        return;
      }

      wlErr.textContent = "";
      wlSubmit.disabled = true;
      wlSubmit.textContent = "Joining\u2026";

      var slow = setTimeout(function () {
        if (wlSubmit.disabled) wlSubmit.textContent = "Still going…";
      }, 4000);

      fetch("/api/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          kind: "waitlist",
          fields: fields,
          confirm_url: (wlForm.elements.confirm_url || {}).value || ""
        })
      }).then(function (r) {
        return r.json().catch(function () { return { ok: false }; });
      }).then(function (out) {
        clearTimeout(slow);
        if (!out || !out.ok) throw new Error((out && out.error) || "That did not go through.");
        wlSubmit.disabled = false;
        wlSubmit.textContent = "Join the waitlist";
        wlForm.hidden = true;
        wlDone.hidden = false;
        joined = true;
      }).catch(function (err) {
        clearTimeout(slow);
        wlSubmit.disabled = false;
        wlSubmit.textContent = "Join the waitlist";
        wlErr.textContent = err.message || "That did not go through. Try again in a moment.";
      });
    });
  }

  /* ---- the thread ----------------------------------------------------- */
  var thread = document.getElementById("lp-thread");
  var input = document.getElementById("lp-input");
  var send = document.getElementById("lp-send");
  if (!thread || !input || !send) return;

  var api = (lp.getAttribute("data-api") || "").replace(/\/+$/, "");
  var token = lp.getAttribute("data-widget-token") || "";
  var session = null;
  var live = false;
  var busy = false;
  var demoTimers = [];
  /* The agent is a demo until we open. Let somebody get a real feel for it --
     long enough to take the brief and come back with roles, which is the part
     worth showing -- then hand them to the waitlist rather than letting the
     conversation run on into nothing. */
  var TURNS_BEFORE_WAITLIST = 12;
  var turns = 0;
  var joined = false;
  var handedOver = false;
  var told = false;

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }
  function bubble(side, text) {
    var b = el("div", "lp-msg " + side, text);
    thread.appendChild(b);
    thread.scrollTop = thread.scrollHeight;
    return b;
  }
  function react(msg, glyph) {
    msg.classList.add("reacted");
    var t = el("span", "lp-react", glyph);
    t.appendChild(el("i"));
    t.appendChild(el("i"));
    msg.appendChild(t);
  }

  /* Tapbacks land where a person would actually reach for one, picked off what
     the message says rather than off its position in the thread -- somebody who
     opens with their name is at a different point from somebody who opens with
     hi. Two in a row reads as a bot with a stuck key, so a reaction normally
     needs a clear turn after the last one. Saying yes and picking a role are
     exempt: those are the two moments a reaction is most worth having, and
     they tend to arrive back to back. */
  var lastReact = -9;
  function reactionFor(text, n) {
    var t = text.trim().toLowerCase();
    var glyph = "", always = false;
    if (/^(ha){2,}$|^(lol|lmao|haha)\b/.test(t)) {
      glyph = "\uD83D\uDE02";
    } else if (/^(yes|yep|yeah|yup|sure|perfect|great|nice|please|do it|go for it|sounds good|let's go)\b/.test(t)) {
      glyph = "\u2764\uFE0F"; always = true;
    } else if (/^(0?[123])\b/.test(t)) {
      glyph = "\u2764\uFE0F"; always = true;              /* picking one of the roles */
    } else if (/\b(asap|urgent|right now|this week|today)\b/.test(t)) {
      glyph = "\u203C\uFE0F";
    } else if (/(linkedin\.com|github\.com|\.pdf|\bresume\b|\bcv\b|\bportfolio\b)/.test(t)) {
      glyph = "\uD83D\uDC40";                             /* something to go and read */
    } else if (/\$|\b\d{3}\s?k\b/.test(t)) {
      glyph = "\uD83D\uDC40";                             /* a number worth a look */
    } else if (/\b(staff|principal|senior|lead|founding|engineer|developer|designer|scientist|analyst)\b/.test(t)) {
      glyph = "\uD83D\uDC4D";
    }
    if (!glyph) return "";
    if (!always && n - lastReact < 2) return "";
    return glyph;
  }

  function typing() {
    var d = el("div", "lp-dots");
    d.innerHTML = "<i></i><i></i><i></i>";
    thread.appendChild(d);
    thread.scrollTop = thread.scrollHeight;
    return d;
  }

  /* The scripted demo. Plays until the visitor types, then gets out of the way. */
  var SCRIPT = [
    [400, "meta", "Today"],
    [700, "me", "hey heard you find jobs over text"],
    [1000, "them", "yep. i'm foray. send your linkedin or a resume and i'll take it from there"],
    [1100, "me", "linkedin.com/in/priya-builds"],
    [1300, "them", "got it. backend, 6 yrs, go + postgres. what comp, and where do you want to be?"],
    [1000, "me", "sf hybrid, 180k+"],
    [1500, "job", ""],
    [1000, "meta-right", "you liked “Senior Backend Engineer · Stripe”"],
    [800, "them", "on it. stripe it is. tailored resume and a short note to the hiring manager. good to go?"],
    [900, "me", "YES"],
    [500, "meta-right", "Read"],
    [1200, "them", "applied. i'll message you the moment they reply"]
  ];

  function jobCard() {
    var thumb = document.getElementById("lp-thumb-src");
    var badge = document.getElementById("lp-stripe-src");
    var badge2 = document.getElementById("lp-anthropic-src");
    var w = el("div", "lp-msg them wide");
    w.innerHTML =
      '<span>found 2 worth your time. like the one you want and i will get your application ready:</span>' +
      '<span class="lp-job">' +
        '<span class="lp-tap" aria-hidden="true">' + (thumb ? thumb.innerHTML : "") + '</span>' +
        '<span class="lp-job-card picked">' +
          '<span class="lp-job-shot">' +
            '<span class="row"><span class="badge">' + (badge ? badge.innerHTML : "") + '</span>' +
            '<span class="co">Jobs at Stripe</span></span>' +
            '<span class="bar"></span><span class="bar short"></span>' +
            '<span class="cta">Apply now</span>' +
          '</span>' +
          '<span class="lp-job-body"><span class="n">01</span>' +
          '<span class="t">Senior Backend Engineer</span>' +
          '<span class="s">SF hybrid · $185–210k</span></span>' +
        '</span>' +
      '</span>' +
      '<span class="lp-job" style="margin-top:8px">' +
        '<span class="lp-job-card">' +
          '<span class="lp-job-shot" style="--shot:#191919">' +
            '<span class="row"><span class="badge">' + (badge2 ? badge2.innerHTML : "") + '</span>' +
            '<span class="co">Careers at Anthropic</span></span>' +
            '<span class="bar"></span><span class="bar short"></span>' +
            '<span class="cta">Apply now</span>' +
          '</span>' +
          '<span class="lp-job-body"><span class="n">02</span>' +
          '<span class="t">Member of Technical Staff</span>' +
          '<span class="s">SF hybrid · $240k + equity</span></span>' +
        '</span>' +
      '</span>';
    thread.appendChild(w);
  }

  function playDemo() {
    var at = 0;
    SCRIPT.forEach(function (step) {
      at += step[0];
      demoTimers.push(setTimeout(function () {
        if (live) return;
        if (step[1] === "meta") thread.appendChild(el("span", "lp-meta", step[2]));
        else if (step[1] === "meta-right") thread.appendChild(el("span", "lp-meta right", step[2]));
        else if (step[1] === "job") jobCard();
        else bubble(step[1], step[2]);
        thread.scrollTop = thread.scrollHeight;
      }, at));
    });
  }

  function goLive() {
    if (live) return;
    live = true;
    demoTimers.forEach(clearTimeout);
    demoTimers = [];
    thread.textContent = "";
    thread.appendChild(el("span", "lp-meta", "Live"));
  }

  /* The moment somebody starts typing, the demo gets out of the way -- and an
     empty box is a bad thing to type into, so Foray says hello while they are
     still composing. On the live path render() redraws from the server
     transcript, so this greeting is only ever the local one. */
  var greeted = false;
  function greet() {
    if (greeted) return;
    greeted = true;
    goLive();
    var dots = typing();
    setTimeout(function () {
      if (dots.parentNode) dots.parentNode.removeChild(dots);
      bubble("them", "hey, i'm foray. tell me what you're after and i'll go find it.");
    }, 650);
  }
  input.addEventListener("input", greet);

  /* The fallback, used only when no widget token is configured or the API is
     unreachable. The asks track the real intake: messaging/identity.py ASKS in
     missing_identity() order (name, then email), then prompts.QUESTIONS in gate
     order. Keep them in step -- a visitor who types here should get the same
     conversation the live thread would give them, minus the part where we
     remember it. The greeting is deliberately not greeting_for()'s: that one
     discloses the agent as an AI because SMS wants it to, and this is a demo
     widget on our own page, where it only reads as throat-clearing. */
  /* The ladder used to be a counter: stage++ on every message, whatever it
     said. So "tg" passed as an email, then as a role, then as a location, and
     three matches with salaries came back off four junk answers -- which reads
     as fake, because it was. Each step now checks the answer to the question it
     asked, and re-asks when it does not fit. The stage only moves on a real
     answer. */
  var stage = 0;
  var brief = { name: "", email: "", role: "", place: "" };

  /* Repeating one sentence word for word is how a form behaves, not a person.
     Each stage keeps its own count and moves down its list. */
  var tries = 0;
  function again(list) { return [list[Math.min(tries++, list.length - 1)]]; }

  var NAME_AGAIN = [
    "a name first, whatever you go by. we'll get to the rest.",
    "anything works. first name is plenty."
  ];
  var EMAIL_AGAIN = [
    "that isn't an address i can reach you at. what's your email?",
    "still need an email. something in the shape of you@company.com.",
    "i can't line anything up without a way to reach you. an email and we're moving."
  ];
  var ROLE_AGAIN = [
    "a bit more than that. backend, infra, ml, product, design, what are you after?",
    "give me the job title you'd want to see on the offer.",
    "even roughly. what kind of engineering do you want to be doing?"
  ];
  var PLACE_AGAIN = [
    "whereabouts? a city is plenty, or remote.",
    "just a city, or say remote and i'll work with that."
  ];

  function letters(t) { return t.replace(/[^a-z]/gi, "").length; }
  function isEmail(t) { return /^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(t); }
  function isLink(t) { return /https?:\/\/|www\.|linkedin\.com|github\.com/i.test(t); }

  /* Their own words, trimmed to something that fits on a card: first clause,
     no trailing punctuation, no sentence-length essays. */
  function tidy(t, cap) {
    t = t.split(/[,.;\n]/)[0].trim().toLowerCase();
    t = t.replace(
      /^(i(?:'m| am)? |i want |looking for |currently |living |based |located |in |at |a |an |the )+/,
      "");
    if (t.length > cap) t = t.slice(0, cap).replace(/\s+\S*$/, "");
    return t;
  }

  function offlineReplies(text) {
    var t = (text || "").trim();

    if (stage === 0) {
      stage = 1;
      return [
        "good to meet you. a few details and i can start matching. couple of minutes, tops.",
        "what name should i put on this?"
      ];
    }

    if (stage === 1) {
      if (isEmail(t) || isLink(t) || letters(t) < 2 || t.length > 60)
        return again(NAME_AGAIN);
      brief.name = tidy(t, 40);
      stage = 2; tries = 0;
      return ["thanks. and the best email to reach you on?"];
    }

    if (stage === 2) {
      /* Never waved through. An address we cannot send to is the one answer
         that makes the whole thread pointless. */
      if (!isEmail(t))
        return again(EMAIL_AGAIN);
      brief.email = t;
      stage = 3; tries = 0;
      return ["what kind of role are you looking for next?"];
    }

    if (stage === 3) {
      if (letters(t) < 4)
        return again(ROLE_AGAIN);
      brief.role = tidy(t, 42);
      stage = 4; tries = 0;
      return ["where are you based, and where would you want to work?"];
    }

    if (stage === 4) {
      if (letters(t) < 2)
        return again(PLACE_AGAIN);
      /* "based in nyc, would do remote" should read as a place on a card, and
         the remote part is the half they actually chose. */
      var place = tidy(t, 24);
      if (/\bremote\b/i.test(t) && place.indexOf("remote") < 0)
        place = place ? place + " or remote" : "remote";
      brief.place = place;
      stage = 5; tries = 0;
      told = true;
      /* Where the page runs out of what it actually knows. Naming roles from
         here would be a guess dressed as a match. */
      return [
        "got it: " + brief.role + ", " + place + ". that's the brief.",
        "i'm not going to make matches up on a landing page. the real thread reads live "
          + "postings and comes back with the ones that actually fit.",
        "join the waitlist and i'll do exactly that the day your spot opens."
      ];
    }

    told = true;
    return ["we're opening spots in batches. join the waitlist and i'll pick this up the day yours is ready."];
  }

  function post(path, body) {
    return fetch(api + path, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    }).then(function (r) {
      if (!r.ok) {
        var e = new Error("http " + r.status);
        e.status = r.status;
        throw e;
      }
      return r.json();
    });
  }
  function clientId() {
    if (window.crypto && crypto.randomUUID) return crypto.randomUUID();
    return "c-" + Date.now().toString(36) + "-" + Math.random().toString(36).slice(2, 8);
  }
  function render(sess) {
    /* The server owns the transcript, so redraw from it rather than appending. */
    thread.textContent = "";
    thread.appendChild(el("span", "lp-meta", "Live"));
    (sess.messages || []).forEach(function (m) {
      if (m && m.body) bubble(m.direction === "inbound" ? "me" : "them", m.body);
    });
  }

  function handOver() {
    handedOver = true;
    input.disabled = true;
    input.placeholder = "Join the waitlist to keep going";
    /* Foray sends the link the way it would send anything else: in the thread,
       as something to tap, rather than as a button floating under it. */
    var card = el("div", "lp-msg them wide lp-wlcard");
    card.setAttribute("role", "button");
    card.setAttribute("tabindex", "0");
    card.innerHTML =
      '<span class="lp-wl-head">' +
        '<span class="lp-logo lp-wl-mark" aria-hidden="true"><b><i></i><i></i><i></i><i></i></b></span>' +
        '<b>Join the waitlist</b></span>' +
      '<span class="lp-wl-sub">Name, email, phone. First 10 applications free.</span>';
    function openWaitlist() {
      var d = document.getElementById("lp-waitlist");
      if (d && d.showModal && !d.open) d.showModal();
    }
    card.addEventListener("click", openWaitlist);
    card.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); openWaitlist(); }
    });
    thread.appendChild(card);
    thread.scrollTop = thread.scrollHeight;
  }

  /* Liking one of the suggestions has to move the conversation on the same way
     typing does, so the thread-advancing half of submit lives here and takes
     the pick as an argument. */
  function submit() {
    var text = input.value.trim();
    if (!text) return;
    input.value = "";
    sendTurn(text);
  }

  function sendTurn(text) {
    if (!text || busy || handedOver) return;
    goLive();
    busy = true;
    turns++;
    var mine = bubble("me", text);
    var glyph = reactionFor(text, turns);
    if (glyph) {
      lastReact = turns;
      setTimeout(function () { react(mine, glyph); }, 1300);
    }
    var dots = typing();

    function offline() {
      var lines = offlineReplies(text);
      lines.forEach(function (line, i) {
        setTimeout(function () {
          if (i === 0 && dots.parentNode) dots.parentNode.removeChild(dots);
          bubble("them", line);
          if (i === lines.length - 1) {
            busy = false;
            maybeHandOver();
          }
        }, 500 + i * 800);
      });
    }

    function maybeHandOver() {
      if (handedOver || joined) return;
      if (!told && turns < TURNS_BEFORE_WAITLIST) return;
      setTimeout(function () {
        /* If they got here by liking a role they have just been told all this. */
        if (!told) {
          bubble("them", "this is the demo, so it stops here. we're opening spots in batches. " +
            "join the waitlist and i'll pick it up for real the day yours is ready.");
        }
        handOver();
      }, 900);
    }

    if (!token || !api) { offline(); return; }

    var open = session
      ? Promise.resolve(session)
      : post("/v1/intake/chat/sessions", { token: token }).then(function (s) { session = s; return s; });

    open.then(function (s) {
      return post("/v1/intake/chat/sessions/" + encodeURIComponent(s.thread_id) + "/messages",
        { token: s.thread_token, body: text, client_message_id: clientId() });
    }).then(function (s) {
      session = s;
      busy = false;
      if (dots.parentNode) dots.parentNode.removeChild(dots);
      render(s);
      maybeHandOver();
    }).catch(function () {
      /* Never strand the visitor mid-sentence: fall back to the script. */
      session = null;
      offline();
    });
  }

  send.addEventListener("click", submit);
  input.addEventListener("keydown", function (e) { if (e.key === "Enter") submit(); });
  input.addEventListener("focus", function () { goLive(); }, { once: true });

  var reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduced) {
    /* No timed reveal: show the conversation as a static transcript. */
    SCRIPT.forEach(function (step) {
      if (step[1] === "me" || step[1] === "them") bubble(step[1], step[2]);
      else if (step[1] === "job") jobCard();
    });
  } else {
    playDemo();
  }
})();