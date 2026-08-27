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

  /* The scripted fallback, used when no widget token is configured or the API
     is unreachable. Same beats as the real intake, so the demo never overstates
     what the product does; it just cannot remember you afterwards. */
  var stage = 0;
  function offlineReplies() {
    var s = stage++;
    if (s === 0) return ["send your linkedin or a resume link and i'll take it from there"];
    if (s === 1) return ["got it. what comp are you after, and where do you want to be?"];
    if (s === 2) return [
      "two worth your time:",
      "01 — senior backend engineer at stripe. sf hybrid, $185–210k",
      "02 — member of technical staff at anthropic. sf hybrid, $240k + equity",
      "reply 1 or 2 and i'll get your application ready"
    ];
    if (s === 3) return ["on it. tailored resume and a short note to the hiring manager. reply YES to send"];
    if (s === 4) return [
      "applied. i'll message you the moment they reply",
      "that's the demo — message foray for the real thing, and your first 10 applications are on us"
    ];
    return ["message foray any time and we pick it up from there"];
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

  function submit() {
    var text = input.value.trim();
    if (!text || busy) return;
    goLive();
    input.value = "";
    busy = true;
    bubble("me", text);
    var dots = typing();

    function offline() {
      var lines = offlineReplies();
      lines.forEach(function (line, i) {
        setTimeout(function () {
          if (i === 0 && dots.parentNode) dots.parentNode.removeChild(dots);
          bubble("them", line);
          if (i === lines.length - 1) busy = false;
        }, 500 + i * 800);
      });
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