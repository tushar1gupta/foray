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
    var open = e.target.closest("[data-open]");
    if (open) {
      var d = document.getElementById(open.getAttribute("data-open"));
      if (d && d.showModal) {
        d.showModal();
        if (d.id === "lp-call") playVoice();
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
        if (!out || !out.ok) throw new Error((out && out.error) || "That did not go through.");
        wlForm.hidden = true;
        wlDone.hidden = false;
        joined = true;
      }).catch(function (err) {
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
     a few turns is enough to see how it answers -- then hand them to the
     waitlist rather than letting the conversation run on into nothing. */
  var TURNS_BEFORE_WAITLIST = 4;
  var turns = 0;
  var joined = false;
  var handedOver = false;

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
    [1000, "meta-right", "you liked “01 Senior Backend Engineer · Stripe”"],
    [800, "them", "on it. stripe it is. tailored resume and a short note to the hiring manager. good to go?"],
    [900, "me", "YES"],
    [500, "meta-right", "Read"],
    [1200, "them", "applied. i'll message you the moment they reply"]
  ];

  function jobCard() {
    var thumb = document.getElementById("lp-thumb-src");
    var badge = document.getElementById("lp-stripe-src");
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
          '<span class="s">SF hybrid · $185–210k</span>' +
          '<span class="u">stripe.com/jobs</span></span>' +
        '</span>' +
      '</span>' +
      '<span class="lp-job" style="margin-top:8px">' +
        '<span class="lp-job-card"><span class="lp-job-body"><span class="n">02</span>' +
        '<span class="t">Member of Technical Staff · Anthropic</span>' +
        '<span class="s">SF hybrid · $240k + equity</span></span></span>' +
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

  /* The fallback, used only when no widget token is configured or the API is
     unreachable. The copy is the real intake's, not an approximation: the
     greeting is messaging/prompts.py greeting_for(), the first two asks are
     messaging/identity.py ASKS in missing_identity() order (name, then email),
     and the rest are prompts.QUESTIONS in gate order. Keep them in step -- a
     visitor who types here should get the same conversation the live thread
     would give them, minus the part where we remember it. */
  var stage = 0;
  function offlineReplies() {
    var s = stage++;
    if (s === 0) return [
      "hey, i'm foray from Foray. i'm an ai, and i'm here to take a few details so we can match you to the right roles. it takes a couple of minutes.",
      "first things first — what name should i put on this?"
    ];
    if (s === 1) return ["and the best email to reach you on?"];
    if (s === 2) return ["what kind of role are you looking for next?"];
    if (s === 3) return ["whereabouts are you based, and which locations would you work in?"];
    if (s === 4) return ["what are you targeting on compensation? base or total is fine."];
    if (s === 5) return [
      "that's the gate closed — on the live line this is where matches start landing in your thread."
    ];
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
    var cta = document.createElement("button");
    cta.type = "button";
    cta.className = "lp-btn";
    cta.style.cssText = "align-self:center; margin-top:6px";
    cta.textContent = "Join the waitlist";
    cta.setAttribute("data-open", "lp-waitlist");
    thread.appendChild(cta);
    thread.scrollTop = thread.scrollHeight;
  }

  function submit() {
    var text = input.value.trim();
    if (!text || busy || handedOver) return;
    goLive();
    input.value = "";
    busy = true;
    turns++;
    bubble("me", text);
    var dots = typing();

    function offline() {
      var lines = offlineReplies();
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
      if (handedOver || joined || turns < TURNS_BEFORE_WAITLIST) return;
      setTimeout(function () {
        bubble("them", "this is the demo, so it stops here. we're opening spots in batches \u2014 " +
          "join the waitlist and i'll pick it up for real the day yours is ready.");
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