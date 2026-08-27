#!/usr/bin/env python3
"""The landing page — markup, styles and behaviour for index.html.

Kept out of ``generate.py`` because it shares nothing with the two form pages:
its own header and footer, its own palette, and a chat widget the other pages
have no use for. ``generate.py`` imports ``CSS``, ``JS`` and ``BODY`` and wraps
them in a bare document; the legacy chrome is deliberately not applied.

The palette is "First light" — dawn purple, chosen against the mint the rest of
the site still uses. When the other two pages are restyled the tokens below
become the shared set and the ``:root`` here can move up into ``generate.py``.

Brand marks for the matched companies are read from ``src/logos`` at build time
and inlined, so the page makes no third-party requests. They identify the
company whose role is being shown; they are not endorsements and must not be
used as a "trusted by" wall.
"""
import pathlib

LOGOS = pathlib.Path(__file__).resolve().parent / "logos"

# Brand colours as published by each company, for the marks only.
LOGO_COLORS = {
    "anthropic": "#191919",
    "openai": "#0F9D77",
    "googlegemini": "#8E75B2",
    "meta": "#0467DF",
    "stripe": "#635BFF",
}


def mark(slug, px):
    """One company mark, re-wrapped at the size the page needs."""
    src = LOGOS.joinpath(slug + ".svg").read_text(encoding="utf-8")
    body = src.split(">", 1)[1].rsplit("</svg>", 1)[0]
    if "<title>" in body:
        body = body.split("</title>", 1)[1]
    return ('<svg width="%d" height="%d" viewBox="0 0 24 24" fill="%s" aria-hidden="true">%s</svg>'
            % (px, px, LOGO_COLORS[slug], body.strip()))


def chip(slug, name, delay):
    """A company row in the match card: mark on a disc, then the name."""
    return ('<li class="lp-chip" style="--d:%ss">'
            '<span class="lp-chip-disc">%s</span><span>%s</span></li>'
            % (delay, mark(slug, 13), name))


CSS = r"""
/* ---- Landing page (First light) ------------------------------------- */
.lp{
  --bg:#FAF8FC; --ink:#2A2140; --muted:#6E6684;
  --primary:#6A50C8; --primary2:#9B7FE0;
  --tint:#EBE4F8; --tint2:#F4F1FA; --tint3:#F9F7FC;
  --sky1:#B08AD6; --sky2:#D7C2EA; --sky3:#F3ECF8;
  --accent:#E8A33C; --accent-soft:#F7DFA9; --accent-deep:#7A5410;
  --band:#241C3B; --band-acc:#E9C36A; --band-acc2:#C9B4EE;
  --line:rgba(42,33,64,.12); --line2:rgba(42,33,64,.2);
  --imsg-in:#E9E9EB; --imsg-out:#0A84FF;
  --wrap:1320px; --gut:clamp(20px,4.4vw,64px);
  background:var(--bg); color:var(--ink);
  font-family:'Schibsted Grotesk',system-ui,-apple-system,sans-serif;
  font-size:clamp(15px,1vw,15.5px); line-height:1.6; letter-spacing:-.005em;
}
.lp *{box-sizing:border-box}
.lp h1,.lp h2,.lp h3{
  font-family:'Bricolage Grotesque','Schibsted Grotesk',system-ui,sans-serif;
  font-weight:600; letter-spacing:-.032em; margin:0; text-wrap:balance;
}
.lp h1{font-size:clamp(34px,5.6vw,62px); line-height:1.05}
.lp h2{font-size:clamp(27px,3.6vw,40px); line-height:1.06}
.lp p{margin:0}
.lp ul{list-style:none; margin:0; padding:0}
.lp a{color:inherit; text-decoration:none}
.lp .wrap{max-width:var(--wrap); margin:0 auto; padding:0 var(--gut)}
.lp .lbl{font-size:11px; font-weight:600; letter-spacing:.16em; text-transform:uppercase}
.lp .mark-hl{background:var(--accent-soft); border-radius:6px; padding:0 .14em}
.lp :focus-visible{outline:2px solid var(--primary); outline-offset:3px}

/* ticker + header */
.lp-ticker{background:var(--primary); color:#fff; text-align:center; padding:9px var(--gut)}
.lp-head{
  display:flex; align-items:center; gap:16px; flex-wrap:wrap;
  max-width:var(--wrap); margin:0 auto; padding:14px var(--gut); border-bottom:1px solid var(--line);
}
.lp-logo{display:inline-flex; align-items:center; gap:12px; font-weight:600; font-size:19px;
  letter-spacing:.2em; text-transform:uppercase; line-height:1}
.lp-logo b{display:grid; grid-template-columns:repeat(2,5px); gap:2.5px}
.lp-logo i{width:5px; height:5px; background:var(--primary); border-radius:1px}
.lp-logo i:nth-child(2){opacity:.5} .lp-logo i:nth-child(3){opacity:.4}
.lp-nav{display:flex; gap:clamp(14px,2vw,28px); margin-left:auto; color:var(--muted)}
.lp-nav a:hover{color:var(--ink)}
.lp-clock{display:flex; gap:10px; margin-left:auto; color:var(--muted); padding-left:20px;
  border-left:1px solid var(--line)}
.lp-clock span{font-variant-numeric:tabular-nums}
@media(max-width:900px){.lp-clock{display:none} .lp-head .lp-btn{margin-left:auto}}

/* buttons */
.lp-btn{display:inline-flex; align-items:center; justify-content:center; gap:8px; cursor:pointer;
  font:inherit; font-size:11.5px; font-weight:600; letter-spacing:.15em; text-transform:uppercase;
  padding:14px 24px; border:0; border-radius:999px; background:var(--primary); color:#fff;
  transition:transform .18s,box-shadow .18s,background .18s}
.lp-btn:hover{transform:translateY(-2px); box-shadow:0 10px 24px rgba(42,33,64,.22)}
.lp-btn.ghost{background:transparent; color:var(--ink); border:1px solid var(--line2)}
.lp-btn.ghost:hover{border-color:var(--primary); color:var(--primary)}
.lp-btn.on-dark{background:#fff; color:var(--ink)}

/* hero */
.lp-hero{background:linear-gradient(180deg,var(--sky2) 0%,var(--sky3) 45%,var(--bg) 100%);
  position:relative; overflow:hidden}
.lp-hero-copy{max-width:var(--wrap); margin:0 auto; padding:clamp(40px,6vw,64px) var(--gut) 0;
  display:flex; flex-direction:column; align-items:center; gap:18px; text-align:center}
.lp-hero-copy h1{max-width:18ch}
.lp-sub{color:var(--muted); font-size:clamp(16px,1.7vw,18px); max-width:56ch}
.lp-stage{position:relative; padding:clamp(28px,4vw,36px) var(--gut) clamp(48px,6vw,64px)}

/* drifting job chips behind the phone */
.lp-drift{position:absolute; inset:0; overflow:hidden; pointer-events:none}
.lp-drift-row{position:absolute; display:flex; width:max-content; will-change:transform}
.lp-drift-row:nth-child(1){top:8%; animation:lp-left 34s linear infinite; opacity:.85}
.lp-drift-row:nth-child(2){top:28%; animation:lp-right 44s linear infinite; opacity:.6}
.lp-drift-row span{background:#fff; border:1px solid var(--line); border-radius:999px;
  padding:8px 16px; font-size:12.5px; color:var(--muted); white-space:nowrap; margin-right:14px}
.lp-drift-row span.hit{border-color:var(--primary); color:var(--primary)}
@keyframes lp-left{from{transform:translateX(0)}to{transform:translateX(-50%)}}
@keyframes lp-right{from{transform:translateX(-50%)}to{transform:translateX(0)}}
@media(max-width:720px){.lp-drift{display:none}}

/* phone */
.lp-phone{position:relative; width:min(400px,100%); margin:0 auto; background:#fff;
  border:1px solid var(--line); border-radius:32px; padding:22px;
  display:flex; flex-direction:column; gap:12px; box-shadow:0 28px 70px rgba(42,33,64,.18)}
.lp-try{position:absolute; top:-16px; right:-14px; z-index:5; transform:rotate(2deg);
  background:var(--primary); color:#fff; border-radius:999px; padding:9px 18px;
  display:flex; align-items:center; gap:7px; font-size:13px; font-weight:600;
  box-shadow:0 10px 24px rgba(42,33,64,.3)}
@media(max-width:520px){.lp-try{right:-4px; font-size:12px; padding:7px 14px}}
.lp-phone-head{display:flex; align-items:center; gap:10px; padding-bottom:12px; border-bottom:1px solid var(--line)}
.lp-phone-head .lp-logo{font-size:12px; gap:8px}
.lp-phone-head .lp-logo b{grid-template-columns:repeat(2,4px); gap:2px}
.lp-phone-head .lp-logo i{width:4px; height:4px}
.lp-live{margin-left:auto; font-size:11.5px; color:var(--muted)}
.lp-thread{display:flex; flex-direction:column; gap:9px; min-height:430px}
.lp-msg{max-width:88%; padding:9px 13px; font-size:13.5px; line-height:1.45; border-radius:18px;
  animation:lp-rise .35s ease both}
.lp-msg.me{align-self:flex-end; background:var(--imsg-out); color:#fff; border-bottom-right-radius:6px}
.lp-msg.them{align-self:flex-start; background:var(--imsg-in); color:#1A1A1A; border-bottom-left-radius:6px}
.lp-msg.wide{max-width:92%; display:flex; flex-direction:column; gap:8px}
.lp-meta{align-self:center; font-size:10.5px; color:#9A9FA4; font-weight:500; animation:lp-rise .35s ease both}
.lp-meta.right{align-self:flex-end}
@keyframes lp-rise{from{opacity:0; transform:translateY(10px)}to{opacity:1; transform:none}}
.lp-dots{align-self:flex-start; background:var(--imsg-in); border-radius:18px 18px 18px 6px;
  padding:11px 14px; display:flex; gap:4px}
.lp-dots i{width:6px; height:6px; border-radius:50%; background:#8E8E93; animation:lp-bounce 1s ease-in-out infinite}
.lp-dots i:nth-child(2){animation-delay:.15s} .lp-dots i:nth-child(3){animation-delay:.3s}
@keyframes lp-bounce{0%,60%,100%{transform:translateY(0);opacity:.4}30%{transform:translateY(-3px);opacity:1}}

/* the job card that reads as a link preview */
.lp-job{position:relative; margin-top:6px}
.lp-job-card{background:#fff; border:1.5px solid var(--line); border-radius:12px; overflow:hidden}
.lp-job-card.picked{border-color:var(--imsg-out); box-shadow:0 0 0 1px var(--imsg-out)}
.lp-job-shot{background:#1A2B4A; padding:10px 12px 12px; display:flex; flex-direction:column; gap:5px}
.lp-job-shot .row{display:flex; align-items:center; gap:6px}
.lp-job-shot .badge{width:15px; height:15px; border-radius:3px; background:#fff; display:grid; place-items:center}
.lp-job-shot .co{color:#fff; font-size:10px; font-weight:600; letter-spacing:.1em; text-transform:uppercase}
.lp-job-shot .bar{height:5px; border-radius:999px; background:rgba(255,255,255,.35)}
.lp-job-shot .bar.short{width:48%; background:rgba(255,255,255,.22)}
.lp-job-shot .cta{align-self:flex-start; margin-top:3px; background:var(--primary); color:#fff;
  border-radius:5px; padding:3px 10px; font-size:9.5px; font-weight:600}
.lp-job-body{padding:9px 12px; display:flex; flex-direction:column; gap:2px}
.lp-job-body .n{font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:10.5px;
  letter-spacing:.14em; color:var(--primary)}
.lp-job-body .t{font-size:13px; font-weight:600}
.lp-job-body .s{font-size:12px; color:var(--muted)}
.lp-job-body .u{font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:10.5px; color:#9AA9B4}
.lp-tap{position:absolute; top:-14px; right:-6px; z-index:2; background:var(--imsg-out);
  border:2px solid #fff; border-radius:999px; padding:3px 8px; display:flex;
  box-shadow:0 3px 8px rgba(42,33,64,.22); animation:lp-pop .4s ease both;
  /* a beat after the card, so it reads as somebody reacting to it */
  animation-delay:1.05s}
@keyframes lp-pop{0%{opacity:0;transform:scale(.3)}70%{opacity:1;transform:scale(1.15)}100%{opacity:1;transform:scale(1)}}
.lp-send{display:flex; gap:8px; align-items:center; border-top:1px solid var(--line); padding-top:12px}
.lp-send input{flex:1; min-width:0; border:1px solid var(--line2); border-radius:999px;
  padding:10px 14px; font:inherit; font-size:13.5px; background:#fff; color:var(--ink)}
.lp-send input:focus{outline:none; border-color:var(--primary)}
.lp-send button{width:36px; height:36px; flex:0 0 auto; border:0; border-radius:50%;
  background:var(--imsg-out); color:#fff; display:grid; place-items:center; cursor:pointer}

/* doors */
.lp-doors{background:#fff; border-bottom:1px solid var(--line)}
.lp-doors .wrap{padding-top:40px; padding-bottom:40px; display:grid; gap:16px;
  grid-template-columns:repeat(auto-fit,minmax(320px,390px)); justify-content:center}
.lp-door{display:flex; align-items:center; gap:16px; padding:22px 24px; border-radius:18px;
  cursor:pointer; text-align:left; font:inherit; border:1px solid transparent;
  transition:transform .2s,box-shadow .2s}
.lp-door:hover{transform:translateY(-3px); box-shadow:0 18px 40px rgba(42,33,64,.18)}
.lp-door .ico{width:44px; height:44px; flex:0 0 auto; border-radius:50%; display:grid; place-items:center}
.lp-door .tt{display:block; font-size:17px; font-weight:600; letter-spacing:-.018em}
.lp-door .ss{display:block; font-size:13.5px}
.lp-door .arw{margin-left:auto; transition:transform .2s}
.lp-door:hover .arw{transform:translateX(5px)}
.lp-door.cand{background:var(--primary); color:#fff; box-shadow:0 14px 34px rgba(106,80,200,.28)}
.lp-door.cand .ico{background:rgba(255,255,255,.16)}
.lp-door.hire{background:#fff; border-color:var(--line2); color:var(--ink)}
.lp-door.hire .ico{background:var(--accent-soft)}
.lp-door.hire .ss{color:var(--muted)}
.lp-free{grid-column:1/-1; justify-self:center; background:var(--accent-soft); color:var(--ink);
  border-radius:6px; padding:8px 18px; font-size:12.5px; font-weight:600}

/* chapters */
.lp-sec{padding:clamp(56px,7vw,88px) 0; border-bottom:1px solid var(--line)}
.lp-sec.alt{background:var(--tint2)}
.lp-sec.white{background:#fff}
.lp-head-row{display:flex; align-items:flex-start; gap:clamp(16px,3vw,28px)}
.lp-num{font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:clamp(34px,5vw,60px);
  font-weight:600; color:var(--primary); opacity:.35; line-height:1}
.lp-kick{color:var(--primary); display:block; margin-bottom:10px}
.lp-grid{display:grid; gap:16px; margin-top:clamp(32px,4vw,48px)}
.lp-g3{grid-template-columns:repeat(auto-fit,minmax(280px,1fr))}
.lp-g4{grid-template-columns:repeat(auto-fit,minmax(230px,1fr))}
.lp-g2{grid-template-columns:repeat(auto-fit,minmax(320px,1fr))}
.lp-card{background:#fff; border:1px solid var(--line); border-radius:16px; padding:24px;
  display:flex; flex-direction:column; gap:14px}
.lp-sec.white .lp-card{background:var(--tint2)}
.lp-card.tap{cursor:pointer; transition:transform .2s,border-color .2s,box-shadow .2s}
.lp-card.tap:hover{transform:translateY(-4px); border-color:var(--primary);
  box-shadow:0 16px 36px rgba(106,80,200,.16)}
.lp-card h3{font-size:17px}
.lp-card .note{color:var(--muted); font-size:12.5px}
.lp-chan-top{display:flex; align-items:center; gap:10px}
.lp-chan-top .lbl{color:var(--primary)}
.lp-chan-val{margin-left:auto; font-size:15px; font-weight:600; color:var(--primary)}
.lp-demo{background:#fff; border:1px solid var(--line); border-radius:16px; padding:14px;
  min-height:128px; display:flex; flex-direction:column; gap:8px}
.lp-sec.white .lp-demo{background:#fff}
.lp-mini{border-radius:12px; padding:6px 11px; font-size:12px; max-width:90%}
.lp-mini.me{align-self:flex-end; background:var(--imsg-out); color:#fff; border-bottom-right-radius:3px}
.lp-mini.them{align-self:flex-start; background:var(--imsg-in); color:#1A1A1A; border-bottom-left-radius:3px}
.lp-wave{display:flex; gap:3px; height:30px; align-items:center; justify-content:center}
.lp-wave i{width:4px; background:var(--primary); border-radius:2px; animation:lp-eq .9s ease-in-out infinite}
@keyframes lp-eq{0%,100%{transform:scaleY(.4)}50%{transform:scaleY(1)}}
.lp-rec{width:9px; height:9px; border-radius:50%; background:#E24C4C; animation:lp-pulse 1.2s ease-in-out infinite}
@keyframes lp-pulse{0%,100%{opacity:1}50%{opacity:.25}}

/* journey */
.lp-track{position:relative; height:56px; margin-top:clamp(28px,4vw,44px)}
.lp-track .rail{position:absolute; left:10%; right:10%; top:26px; height:2px;
  background:repeating-linear-gradient(90deg,var(--line2) 0 6px,transparent 6px 14px)}
.lp-track .stop{position:absolute; top:22px; width:10px; height:10px; margin-left:-5px;
  border-radius:50%; background:var(--primary)}
.lp-track .stop.last{background:var(--accent)}
.lp-walker{position:absolute; top:8px; margin-left:-19px; width:38px; height:38px; border-radius:50%;
  background:var(--primary); border:3px solid #fff; display:grid; place-items:center;
  box-shadow:0 6px 16px rgba(42,33,64,.35); animation:lp-walk 9s ease-in-out infinite}
.lp-walker-arrow{position:absolute; top:16px; margin-left:24px; color:var(--primary);
  animation:lp-walk 9s ease-in-out infinite}
@keyframes lp-walk{
  0%{left:12.5%;opacity:1}10%{left:12.5%}26%{left:37.5%}36%{left:37.5%}
  52%{left:62.5%}62%{left:62.5%}78%{left:87.5%}92%{left:87.5%;opacity:1}
  95%{left:87.5%;opacity:0}97%{left:12.5%;opacity:0}100%{left:12.5%;opacity:1}}
.lp-conf{position:absolute; left:87.5%; top:0}
.lp-conf i{position:absolute; width:6px; height:6px; border-radius:50%;
  animation:lp-conf 9s ease-out infinite}
@keyframes lp-conf{0%,76%{opacity:0;transform:translate(0,0) rotate(0)}
  80%{opacity:1}94%{opacity:0;transform:translate(var(--tx),var(--ty)) rotate(240deg)}100%{opacity:0}}
.lp-jcard{animation-duration:9s; animation-timing-function:ease; animation-fill-mode:both;
  animation-iteration-count:infinite}
.lp-jcard:nth-child(1){animation-name:lp-rev1}
.lp-jcard:nth-child(2){animation-name:lp-rev2}
.lp-jcard:nth-child(3){animation-name:lp-rev3}
.lp-jcard:nth-child(4){animation-name:lp-rev4}
@keyframes lp-rev1{0%,2%{opacity:0;transform:translateY(14px)}7%{opacity:1;transform:none}96%{opacity:1}100%{opacity:0}}
@keyframes lp-rev2{0%,24%{opacity:0;transform:translateY(14px)}29%{opacity:1;transform:none}96%{opacity:1}100%{opacity:0}}
@keyframes lp-rev3{0%,50%{opacity:0;transform:translateY(14px)}55%{opacity:1;transform:none}96%{opacity:1}100%{opacity:0}}
@keyframes lp-rev4{0%,76%{opacity:0;transform:translateY(14px)}81%{opacity:1;transform:none}96%{opacity:1}100%{opacity:0}}
.lp-pill{display:inline-flex; align-items:center; gap:6px; background:var(--tint);
  color:var(--primary); border-radius:999px; padding:4px 10px; font-size:11px; font-weight:600}
.lp-tags{display:flex; flex-wrap:wrap; gap:6px}
.lp-tags span{background:var(--tint); border-radius:999px; padding:4px 11px; font-size:11.5px; font-weight:600}
.lp-range{position:relative; height:6px; background:var(--line); border-radius:999px; display:block}
.lp-range i{position:absolute; left:35%; right:20%; top:0; bottom:0; background:var(--primary); border-radius:999px}
.lp-range b{position:absolute; top:-4px; width:14px; height:14px; border-radius:50%;
  background:#fff; border:2.5px solid var(--primary)}
.lp-chip{display:flex; align-items:center; gap:9px; background:#fff; border:1px solid var(--line);
  border-radius:999px; padding:6px 12px; font-size:12.5px; font-weight:600;
  animation:lp-chipin 9s ease both infinite; animation-delay:var(--d)}
.lp-sec.white .lp-chip{background:var(--tint2)}
@keyframes lp-chipin{0%,55%{opacity:0;transform:scale(.7)}60%{opacity:1;transform:scale(1)}96%{opacity:1}100%{opacity:0}}
.lp-chip-disc{width:22px; height:22px; flex:0 0 auto; border-radius:50%; background:#fff;
  border:1px solid var(--line); display:grid; place-items:center}
.lp-cal{background:var(--accent-soft); border-radius:12px; padding:12px; display:flex; gap:12px; align-items:center}
.lp-cal .day{background:#fff; border-radius:10px; padding:8px 12px; display:flex; flex-direction:column;
  align-items:center; box-shadow:0 4px 10px rgba(42,33,64,.1)}
.lp-cal .day em{font-style:normal; font-size:9px; font-weight:700; letter-spacing:.14em;
  text-transform:uppercase; color:#E24C4C}
.lp-cal .day strong{font-size:19px; line-height:1.1}

/* agent-at-work */
.lp-flow{display:grid; gap:16px; align-items:center; margin-top:clamp(32px,4vw,48px);
  grid-template-columns:minmax(0,240px) 40px minmax(0,1fr) 40px minmax(0,240px)}
@media(max-width:980px){.lp-flow{grid-template-columns:1fr}.lp-flow .arw{display:none}}
.lp-flow .arw{color:var(--primary); justify-self:center}
.lp-flow .arw path{stroke-dasharray:4 5; animation:lp-dash .9s linear infinite}
@keyframes lp-dash{to{stroke-dashoffset:-18}}
.lp-browser{background:#fff; border:1px solid var(--line); border-radius:14px; overflow:hidden;
  box-shadow:0 18px 44px rgba(42,33,64,.1)}
.lp-browser-bar{display:flex; align-items:center; gap:8px; padding:10px 14px; background:var(--tint2);
  border-bottom:1px solid var(--line)}
.lp-browser-bar i{width:9px; height:9px; border-radius:50%; background:var(--line2)}
.lp-url{margin-left:8px; font-family:ui-monospace,SFMono-Regular,Menlo,monospace;
  font-size:11.5px; color:var(--muted); overflow:hidden; text-overflow:ellipsis; white-space:nowrap}
.lp-agent-tag{margin-left:auto; display:flex; align-items:center; gap:6px; background:var(--accent-soft);
  color:var(--accent-deep); border-radius:999px; padding:4px 10px; font-size:10px; font-weight:700;
  letter-spacing:.12em; text-transform:uppercase; white-space:nowrap}
.lp-form{position:relative; padding:18px 20px; display:flex; flex-direction:column; gap:10px}
.lp-row{display:flex; align-items:flex-start; gap:12px}
.lp-row .k{width:96px; flex:0 0 auto; font-size:11px; font-weight:600; letter-spacing:.1em;
  text-transform:uppercase; color:var(--muted); padding-top:8px}
.lp-row .v{flex:1; min-width:0; overflow:hidden; background:var(--tint3); border:1px solid var(--line);
  border-radius:8px; padding:7px 12px; font-size:13px}
.lp-type{display:inline-block; overflow:hidden; white-space:nowrap; vertical-align:bottom;
  max-width:0; animation-duration:7s; animation-timing-function:steps(24); animation-iteration-count:infinite;
  animation-fill-mode:both}
/* One step per character, and a target the width of the actual string --
   a generous target reaches full width in the first step or two, which reads
   as a jump rather than typing, and takes the nib with it in one hop. */
.lp-type.t1{animation-name:lp-t1; animation-timing-function:steps(8)}
.lp-type.t2{animation-name:lp-t2; animation-timing-function:steps(23)}
.lp-type.t3{animation-name:lp-t3; animation-timing-function:steps(40)}
@keyframes lp-t1{0%,6%{max-width:0}16%,100%{max-width:9ch}}
@keyframes lp-t2{0%,22%{max-width:0}34%,100%{max-width:24ch}}
@keyframes lp-t3{0%,48%{max-width:0}64%,100%{max-width:100%}}
.lp-pillin{animation:lp-pillin 7s ease both infinite}
@keyframes lp-pillin{0%,38%{opacity:0;transform:scale(.6)}42%{opacity:1;transform:scale(1)}100%{opacity:1}}
/* The nib sits inline directly after the text it is writing, so it travels
   with the characters instead of hovering at the edge of the field. One per
   row, each shown only while that row is being filled. */
.lp-nib{display:inline-flex; align-items:center; gap:5px; vertical-align:middle;
  margin-left:6px; opacity:0; animation-duration:7s; animation-timing-function:ease;
  animation-iteration-count:infinite; animation-fill-mode:both}
.lp-nib b{background:var(--accent-soft); color:var(--accent-deep); border-radius:5px;
  padding:2px 6px; font-size:9px; font-weight:700; letter-spacing:.08em; text-transform:uppercase}
.lp-nib i{width:22px; height:22px; flex:0 0 auto; border-radius:6px; background:var(--primary);
  display:grid; place-items:center; box-shadow:0 4px 10px rgba(42,33,64,.3)}
.lp-nib.n1{animation-name:lp-nib1} .lp-nib.n2{animation-name:lp-nib2}
.lp-nib.n3{animation-name:lp-nib3} .lp-nib.n4{animation-name:lp-nib4}
@keyframes lp-nib1{0%,5%{opacity:0}7%,17%{opacity:1}19%,100%{opacity:0}}
@keyframes lp-nib2{0%,21%{opacity:0}23%,35%{opacity:1}37%,100%{opacity:0}}
@keyframes lp-nib4{0%,37%{opacity:0}39%,45%{opacity:1}47%,100%{opacity:0}}
@keyframes lp-nib3{0%,47%{opacity:0}49%,65%{opacity:1}67%,100%{opacity:0}}
.lp-progress{flex:1; height:6px; background:var(--line); border-radius:999px; overflow:hidden}
.lp-progress i{display:block; height:100%; width:4%; background:var(--primary); border-radius:999px;
  animation:lp-fill 7s ease-in-out infinite}
@keyframes lp-fill{0%,66%{width:4%}90%{width:96%}100%{width:96%}}
.lp-assure{display:flex; flex-wrap:wrap; justify-content:center; gap:16px 40px;
  border-top:1px solid var(--line); margin-top:clamp(28px,4vw,44px); padding-top:28px}
.lp-assure li{display:flex; align-items:center; gap:10px; color:var(--muted); font-size:14px}

/* companies */
.lp-band{background:var(--band); color:#fff}
.lp-band h2{color:#fff; max-width:22ch}
.lp-band .wrap{padding-top:clamp(56px,7vw,88px); padding-bottom:clamp(56px,7vw,88px)}
.lp-band-intro{display:flex; flex-direction:column; align-items:center; gap:14px; text-align:center}
.lp-band-intro .lbl{color:var(--band-acc)}
.lp-band-intro p{color:rgba(255,255,255,.75); font-size:clamp(15px,1.7vw,17px); max-width:54ch}
.lp-stats{display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:24px;
  border-top:1px solid rgba(255,255,255,.14); border-bottom:1px solid rgba(255,255,255,.14);
  padding:28px 0; margin:clamp(32px,4vw,48px) 0; text-align:center}
.lp-stats b{display:block; font-size:clamp(28px,3.4vw,34px); font-weight:600;
  letter-spacing:-.032em; color:var(--band-acc)}
.lp-stats span{color:rgba(255,255,255,.75)}
.lp-steps{display:grid; gap:16px; grid-template-columns:repeat(auto-fit,minmax(280px,1fr))}
.lp-step{background:rgba(255,255,255,.06); border:1px solid rgba(255,255,255,.14); border-radius:16px;
  padding:26px; display:flex; flex-direction:column; gap:12px; cursor:pointer;
  transition:transform .2s,border-color .2s; animation:lp-rise .5s ease both}
.lp-step:hover{transform:translateY(-3px); border-color:var(--band-acc)}
.lp-step .lbl{color:var(--band-acc)}
.lp-step h3{color:#fff}
.lp-step p{color:rgba(255,255,255,.7); font-size:13.5px}
.lp-mini-panel{background:rgba(255,255,255,.06); border:1px solid rgba(255,255,255,.12);
  border-radius:12px; padding:12px; display:flex; flex-direction:column; gap:8px}
.lp-out{display:flex; align-items:center; gap:8px}
.lp-out .av{width:22px; height:22px; flex:0 0 auto; border-radius:50%; display:grid; place-items:center;
  font-size:9.5px; font-weight:700}
.lp-out .ln{flex:1; height:7px; border-radius:999px; background:rgba(255,255,255,.2)}
.lp-out .st{background:rgba(255,255,255,.14); color:var(--band-acc); border-radius:999px;
  padding:2px 9px; font-size:10px; font-weight:700; letter-spacing:.08em}
.lp-week{display:grid; grid-template-columns:repeat(5,1fr); gap:6px}
.lp-week .d{text-align:center; font-size:9px; font-weight:700; letter-spacing:.1em; color:rgba(255,255,255,.55)}
.lp-week .c{height:34px; border-radius:7px; background:rgba(255,255,255,.07); display:grid;
  place-items:center; font-size:9.5px; font-weight:700}
.lp-ledger{display:flex; flex-direction:column; gap:8px}
.lp-ledger div{display:flex; align-items:center; gap:9px; font-size:12.5px}
.lp-ledger div+div{border-top:1px solid rgba(255,255,255,.1); padding-top:8px}
.lp-ledger .amt{margin-left:auto; font-weight:700}
/* The one row that is a good outcome gets to look like one: lifted off the
   panel and warmed, rather than sharing the flat treatment of the two nils. */
.lp-ledger .win{background:rgba(233,195,106,.14); border:1px solid rgba(233,195,106,.35);
  border-radius:10px; padding:9px 11px; margin:-2px 0 2px; color:#fff}
.lp-ledger .win+div{border-top:0; padding-top:0}
.lp-ledger .tick{width:20px; height:20px; flex:0 0 auto; border-radius:50%;
  background:var(--band-acc); display:grid; place-items:center}
.lp-funnel{background:rgba(255,255,255,.06); border:1px solid rgba(255,255,255,.14);
  border-radius:16px; padding:clamp(20px,3vw,32px); margin-top:16px}
.lp-funnel-top{display:flex; justify-content:space-between; gap:16px; color:rgba(255,255,255,.7)}
.lp-funnel-top .hit{color:var(--band-acc)}
.lp-bars{display:flex; align-items:flex-end; gap:3px; height:96px; margin-top:18px}
.lp-bars i{flex:1 1 auto; min-width:2px; background:rgba(255,255,255,.25); border-radius:2px}
.lp-bars i.hit{background:var(--band-acc); box-shadow:0 0 12px rgba(233,195,106,.5)}
.lp-funnel-foot{display:flex; justify-content:space-between; gap:16px; flex-wrap:wrap;
  border-top:1px solid rgba(255,255,255,.12); margin-top:16px; padding-top:12px;
  font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:12px; color:rgba(255,255,255,.7)}
.lp-booking{background:#fff; color:var(--ink); border-radius:18px; padding:clamp(28px,4vw,44px);
  display:flex; flex-wrap:wrap; align-items:center; gap:24px; margin-top:clamp(32px,4vw,48px)}
.lp-booking .t{flex:1; min-width:260px; display:flex; flex-direction:column; gap:8px}
.lp-booking .t b{font-size:clamp(20px,2.6vw,26px); font-weight:600; letter-spacing:-.024em}
.lp-booking .t span{color:var(--muted); font-size:15px; max-width:52ch}
.lp-booking .a{display:flex; flex-direction:column; align-items:flex-end; gap:10px}
.lp-booking .a small{font-family:ui-monospace,SFMono-Regular,Menlo,monospace; color:var(--muted)}

/* closer + footer */
.lp-closer{padding:clamp(56px,8vw,96px) 0; text-align:center;
  background:linear-gradient(180deg,var(--bg) 0%,var(--tint) 100%); border-bottom:1px solid var(--line)}
.lp-closer .acts{display:flex; flex-wrap:wrap; gap:12px; justify-content:center; margin-top:28px}
.lp-foot{padding:clamp(40px,5vw,56px) 0 40px}
.lp-fcols{display:grid; grid-template-columns:1.4fr repeat(3,1fr); gap:32px}
@media(max-width:820px){.lp-fcols{grid-template-columns:1fr 1fr}}
.lp-fcols h4{color:var(--muted); margin:0 0 16px; font-size:11px; font-weight:700;
  letter-spacing:.16em; text-transform:uppercase}
.lp-fcols li{padding:5px 0}
.lp-fcols button{background:none; border:0; padding:0; font:inherit; color:inherit; cursor:pointer; text-align:left}
.lp-fcols button:hover{color:var(--primary)}
.lp-fbot{display:flex; flex-wrap:wrap; gap:14px 30px; justify-content:space-between; color:var(--muted);
  border-top:1px solid var(--line); margin-top:clamp(32px,4vw,48px); padding-top:22px}

/* dialogs */
.lp-modal{border:0; padding:0; background:transparent; max-width:min(480px,92vw)}
.lp-modal::backdrop{background:rgba(20,14,40,.5)}
.lp-modal .box{background:#fff; border-radius:22px; padding:clamp(24px,4vw,36px); position:relative;
  display:flex; flex-direction:column; gap:16px; box-shadow:0 30px 80px rgba(20,14,40,.35)}
.lp-modal .x{position:absolute; top:16px; right:16px; width:32px; height:32px; border:0; cursor:pointer;
  border-radius:50%; background:var(--tint2); display:grid; place-items:center}
.lp-modal .big{font-size:clamp(26px,4vw,34px); font-weight:700; letter-spacing:-.02em; color:var(--primary);
  font-family:'Bricolage Grotesque',system-ui,sans-serif}
.lp-modal h3{font-size:clamp(20px,3vw,26px); font-weight:600; letter-spacing:-.024em}
.lp-modal p{color:var(--muted); font-size:14px}
.lp-modal .acts{display:flex; flex-wrap:wrap; align-items:center; gap:12px}
.lp-month{background:var(--tint2); border:1px solid var(--line); border-radius:14px; padding:16px;
  display:flex; flex-direction:column; gap:10px}
.lp-month .hdr{display:flex; justify-content:space-between; align-items:center; font-size:13px; font-weight:700}
.lp-month .hdr span{font-weight:400; font-size:11px; color:var(--muted)}
.lp-days{display:grid; grid-template-columns:repeat(7,1fr); gap:5px}
.lp-days span{text-align:center; padding:6px 0; font-size:12px; color:var(--muted); border-radius:8px}
.lp-days span.sel{background:var(--primary); color:#fff; font-weight:700}
.lp-times{display:flex; gap:8px}
.lp-times span{flex:1; text-align:center; border:1px solid var(--line2); border-radius:999px;
  padding:7px 0; font-size:12px; color:var(--muted)}
.lp-times span.sel{border:1.5px solid var(--primary); color:var(--primary); font-weight:700}

@media (prefers-reduced-motion:reduce){
  .lp *,.lp *::before,.lp *::after{animation-duration:.01ms!important; animation-iteration-count:1!important;
    transition-duration:.01ms!important}
  .lp-jcard,.lp-chip,.lp-msg,.lp-meta,.lp-step{opacity:1!important; transform:none!important}
}
"""


JS = r"""
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
      "that's the gate closed — on the live line this is where matches start landing in your thread.",
      "this page is running the demo script, so nothing here is saved. message foray for the real thing."
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
"""


# ---- icons -----------------------------------------------------------------

def _svg(paths, size=20, stroke="currentColor", extra=""):
    return ('<svg width="%d" height="%d" viewBox="0 0 24 24" fill="none" stroke="%s" '
            'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" '
            'aria-hidden="true"%s>%s</svg>' % (size, size, stroke, extra, paths))


I = {
    "chat": '<path d="M21 11.5a8.38 8.38 0 0 1-8.5 8.5 8.5 8.5 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 8.5-8.5 8.38 8.38 0 0 1 8.5 8.5Z"/>',
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92Z"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
    "user": '<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
    "team": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "arrow": '<path d="M5 12h14"/><path d="m13 6 6 6-6 6"/>',
    "down": '<path d="M12 5v14"/><path d="m19 12-7 7-7-7"/>',
    "up": '<path d="M12 19V5"/><path d="m5 12 7-7 7 7"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "x": '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    "doc": '<path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/>',
    "pen": '<path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z"/>',
    "eye": '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/>',
    "speaker": '<polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/>',
    "send": '<path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/>',
    "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "megaphone": '<path d="m3 11 18-5v12L3 14v-3z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/>',
    "coin": '<circle cx="12" cy="12" r="10"/><path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"/><path d="M12 6v2m0 8v2"/>',
    "bolt": '<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>',
    "thumb": '<path d="M7 10v12"/><path d="M15 5.88 14 10h5.83a2 2 0 0 1 1.92 2.56l-2.33 8A2 2 0 0 1 17.5 22H4a2 2 0 0 1-2-2v-8a2 2 0 0 1 2-2h2.76a2 2 0 0 0 1.79-1.11L12 2a3.13 3.13 0 0 1 3 3.88Z"/>',
}

LOGOMARK = '<b aria-hidden="true"><i></i><i></i><i></i><i></i></b>'

# Roles that drift behind the phone. Real companies and real bands, because a
# made-up ladder is the first thing an engineer would catch.
DRIFT_A = [
    ("Research Engineer · Google DeepMind", "$230k", False),
    ("Software Engineer, Platform · Tesla", "$195k", False),
    ("Senior Backend Engineer · Stripe", "$185–210k", True),
    ("Infra Engineer · OpenAI", "$250k", False),
    ("Member of Technical Staff · Anthropic", "$240k + equity", False),
]
DRIFT_B = [
    ("Platform Engineer · Microsoft", "$190k", False),
    ("Product Engineer · Notion", "$185k", False),
    ("Data Platform · Databricks", "$205k", False),
    ("Senior Fullstack · Figma", "$180k", False),
]


def _drift(items):
    one = "".join('<span%s>%s · %s</span>' % (' class="hit"' if hit else "", role, pay)
                  for role, pay, hit in items)
    # Doubled so the -50% translate loops without a seam.
    return '<div class="lp-drift-row">%s%s</div>' % (one, one)


def _bars():
    """The funnel: everyone who could do the job, five who reach the calendar."""
    import math
    hits = {6, 18, 30, 43, 56}
    out = []
    for i in range(64):
        if i in hits:
            out.append('<i class="hit" style="height:92px"></i>')
        else:
            h = round(22 + 54 * abs(math.sin(i * 2.7)))
            out.append('<i style="height:%dpx"></i>' % h)
    return "".join(out)


BODY = """
<div class="lp" data-api="https://app.goforay.io" data-widget-token="">

  <div class="lp-ticker lbl">New: apply to your next role by text, call, or email · first 10 applications on us</div>

  <header class="lp-head">
    <a href="index.html" class="lp-logo" aria-label="Foray home">{logomark}Foray</a>
    <div class="lp-clock lbl"><span>San Francisco</span><span id="lp-clk">--:--</span></div>
    <button type="button" class="lp-btn" data-open="lp-text">Message Foray</button>
  </header>

  <main>
    <section class="lp-hero">
      <div class="lp-hero-copy">
        <h1>Your <em class="mark-hl">autonomous</em> recruiting agent.</h1>
        <p class="lp-sub">Foray finds roles worth your time, writes the application, and applies for
          you. A human reviews everything, and nothing sends without your yes.</p>
      </div>

      <div class="lp-stage">
        <div class="lp-drift" aria-hidden="true">{drift_a}{drift_b}</div>

        <div class="lp-phone" id="lp-phone">
          <span class="lp-try">Try it now, type below {icon_down}</span>
          <div class="lp-phone-head">
            <span class="lp-logo" aria-hidden="true">{logomark}Foray</span>
            <span class="lp-live">Active now</span>
          </div>
          <div class="lp-thread" id="lp-thread" role="log" aria-live="polite"
               aria-label="Conversation with Foray"></div>
          <div class="lp-send">
            <label class="lp-sr" for="lp-input" hidden>Message Foray</label>
            <input id="lp-input" type="text" maxlength="4000" autocomplete="off"
                   placeholder="Message Foray — try anything">
            <button type="button" id="lp-send" aria-label="Send">{icon_up_w}</button>
          </div>
        </div>
      </div>
    </section>

    <section class="lp-doors">
      <div class="wrap">
        <button type="button" class="lp-door cand" data-open="lp-text">
          <span class="ico">{icon_chat_w}</span>
          <span><span class="tt">I&rsquo;m a candidate</span>
            <span class="ss">Message Foray &middot; replies in minutes</span></span>
          <span class="arw" aria-hidden="true">{icon_arrow_w}</span>
        </button>
        <button type="button" class="lp-door hire" data-open="lp-hire">
          <span class="ico">{icon_team_a}</span>
          <span><span class="tt">I&rsquo;m hiring</span>
            <span class="ss">Book 20 minutes &middot; success fee only</span></span>
          <span class="arw" aria-hidden="true">{icon_arrow_a}</span>
        </button>
        <span class="lp-free">10 applications, free</span>
      </div>
    </section>

    <section class="lp-sec white">
      <div class="wrap">
        <div class="lp-head-row">
          <span class="lp-num" aria-hidden="true">01</span>
          <div>
            <span class="lp-kick lbl">For candidates &middot; Ways in</span>
            <h2>Start wherever you already are.</h2>
          </div>
        </div>
        <div class="lp-grid lp-g3">

          <button type="button" class="lp-card tap" data-open="lp-text">
            <span class="lp-chan-top">{icon_chat_p}<span class="lbl">Text</span>
              <span class="lp-chan-val">Message Foray</span></span>
            <span class="lp-demo">
              <span class="lp-mini me">hey, looking for a role</span>
              <span class="lp-mini them">2 matches already. sending now</span>
              <span class="lp-dots" style="align-self:flex-start"><i></i><i></i><i></i></span>
            </span>
            <span class="note">Fastest. Matches land in the same thread.</span>
          </button>

          <button type="button" class="lp-card tap" data-open="lp-call">
            <span class="lp-chan-top">{icon_phone_p}<span class="lbl">Call</span>
              <span class="lp-chan-val">Request a call</span></span>
            <span class="lp-demo" style="justify-content:center; gap:12px">
              <span style="display:flex; align-items:center; gap:10px">
                <span class="lp-rec"></span><span style="font-size:12.5px; font-weight:600">foray &middot; voice</span>
                <span style="margin-left:auto; font-size:12px; color:var(--muted)">00:42</span>
              </span>
              <span class="lp-wave">{wave}</span>
              <span style="font-size:11.5px; color:var(--muted); text-align:center">
                &ldquo;&hellip;180k plus, hybrid in SF&rdquo; &middot; noted</span>
            </span>
            <span class="note">Three minutes with Foray. You talk, we take notes.</span>
          </button>

        </div>
      </div>
    </section>

    <section class="lp-sec alt">
      <div class="wrap">
        <div class="lp-head-row">
          <span class="lp-num" aria-hidden="true">02</span>
          <div>
            <span class="lp-kick lbl">For candidates &middot; Hello to interview</span>
            <h2>Speedrun the process.</h2>
          </div>
        </div>

        <div class="lp-track" aria-hidden="true">
          <span class="rail"></span>
          <span class="stop" style="left:12.5%"></span>
          <span class="stop" style="left:37.5%"></span>
          <span class="stop" style="left:62.5%"></span>
          <span class="stop last" style="left:87.5%"></span>
          <span class="lp-walker">{icon_user_w}</span>
          <span class="lp-walker-arrow">{icon_arrow_sm}</span>
          <span class="lp-conf">
            <i style="--tx:-26px;--ty:-34px;background:var(--accent)"></i>
            <i style="--tx:24px;--ty:-40px;background:var(--primary2)"></i>
            <i style="--tx:-38px;--ty:-12px;background:var(--primary)"></i>
            <i style="--tx:38px;--ty:-16px;background:var(--accent-soft)"></i>
            <i style="--tx:-14px;--ty:-48px;background:var(--primary2)"></i>
            <i style="--tx:12px;--ty:-52px;background:var(--accent)"></i>
          </span>
        </div>

        <div class="lp-grid lp-g4">
          <div class="lp-card lp-jcard">
            <span class="lbl" style="color:var(--primary)">Say hi</span>
            <span class="lp-demo" style="min-height:0">
              <span class="lp-mini me">linkedin.com/in/priya-builds</span>
              <span class="lp-mini them">got it, priya</span>
              <span class="lp-pill" style="align-self:flex-end">{icon_doc_p} resume.pdf</span>
            </span>
            <span class="note">A profile or a resume is the whole application.</span>
          </div>

          <div class="lp-card lp-jcard">
            <span class="lbl" style="color:var(--primary)">Tell us your ask</span>
            <span class="lp-demo" style="min-height:0; gap:12px">
              <span class="lp-tags"><span>$180k+</span><span>SF hybrid</span><span>Go + Postgres</span></span>
              <span style="display:flex; flex-direction:column; gap:6px">
                <span style="display:flex; justify-content:space-between; font-size:10.5px; color:var(--muted)">
                  <span>Comp target</span><span style="color:var(--primary); font-weight:700">$180k–220k</span></span>
                <span class="lp-range"><i></i><b style="left:35%; margin-left:-7px"></b><b style="right:20%; margin-right:-7px"></b></span>
              </span>
            </span>
            <span class="note">Three minutes, once. We remember.</span>
          </div>

          <div class="lp-card lp-jcard">
            <span class="lbl" style="color:var(--primary)">We match, fast</span>
            <ul style="display:flex; flex-direction:column; gap:6px">{chips}</ul>
            <span class="note">Matches in your thread within minutes.</span>
          </div>

          <div class="lp-card lp-jcard" style="border-color:var(--accent)">
            <span class="lbl" style="color:var(--accent-deep)">You interview</span>
            <span class="lp-cal">
              <span class="day"><em>Thu</em><strong>11:00</strong></span>
              <span style="display:flex; flex-direction:column; gap:2px">
                <span style="display:flex; align-items:center; gap:6px; font-size:13px; font-weight:700">
                  {icon_check_p} Interview scheduled</span>
                <span style="font-size:12px; color:var(--muted)">Senior Backend Engineer &middot; Stripe</span>
              </span>
            </span>
            <span class="note">You said yes and we did the rest. Now it&rsquo;s on your calendar.</span>
          </div>
        </div>
        <p class="note" style="text-align:center; margin-top:24px; color:var(--muted)">
          Nothing reaches a company without your say. Timeline, location, visa status, and comp are yours to set.</p>
      </div>
    </section>

    <section class="lp-sec white">
      <div class="wrap">
        <div class="lp-head-row">
          <span class="lp-num" aria-hidden="true">03</span>
          <div>
            <span class="lp-kick lbl">For candidates &middot; The agent at work</span>
            <h2>Meet your AI-native recruiter.</h2>
            <span style="display:flex; align-items:center; gap:10px; margin-top:12px">
              <span style="width:36px;height:36px;border-radius:9px;background:var(--primary);display:grid;place-items:center">{icon_bolt_w}</span>
              <span style="display:flex; flex-direction:column; line-height:1.3">
                <span style="font-size:14px; font-weight:700">foray</span>
                <span style="font-size:12px; color:var(--muted)">your recruiter, at work below</span></span>
            </span>
          </div>
        </div>

        <div class="lp-flow">
          <div class="lp-card">
            <span class="lbl" style="color:var(--muted)">In your thread</span>
            <span class="lp-mini me" style="align-self:flex-end; font-weight:700">YES</span>
            <span class="note">One word from you is the green light.</span>
          </div>
          <span class="arw" aria-hidden="true">{icon_flow}</span>

          <div class="lp-browser">
            <div class="lp-browser-bar">
              <i></i><i></i><i></i>
              <span class="lp-url">stripe.com/jobs/apply</span>
              <span class="lp-agent-tag">{icon_bolt_a} foray agent typing</span>
            </div>
            <div class="lp-form">
              <div class="lp-row"><span class="k">Name</span>
                <span class="v"><span class="lp-type t1">Priya S.</span><span class="lp-nib n1" aria-hidden="true"><b>foray</b><i>{icon_pen_w}</i></span></span></div>
              <div class="lp-row"><span class="k">Role</span>
                <span class="v"><span class="lp-type t2">Senior Backend Engineer</span><span class="lp-nib n2" aria-hidden="true"><b>foray</b><i>{icon_pen_w}</i></span></span></div>
              <div class="lp-row"><span class="k">Resume</span>
                <span class="v" style="background:none; border:0; padding:0">
                  <span class="lp-pill lp-pillin">{icon_doc_p} priya_stripe_tailored.pdf</span><span class="lp-nib n4" aria-hidden="true"><b>foray</b><i>{icon_pen_w}</i></span></span></div>
              <div class="lp-row"><span class="k">Note</span>
                <span class="v" style="color:var(--muted); font-size:12.5px">
                  <span class="lp-type t3">Six years of Go and Postgres, owned a payments system&hellip;</span><span class="lp-nib n3" aria-hidden="true"><b>foray</b><i>{icon_pen_w}</i></span></span></div>
              <div class="lp-row" style="align-items:center; padding-top:4px">
                <span class="k" aria-hidden="true"></span>
                <span class="lp-progress"><i></i></span>
                <span style="font-family:ui-monospace,monospace; font-size:11px; color:var(--primary)">submitting&hellip;</span>
              </div>
            </div>
          </div>

          <span class="arw" aria-hidden="true">{icon_flow}</span>
          <div class="lp-card">
            <span class="lbl" style="color:var(--muted)">Back in your thread</span>
            <span class="lp-mini them" style="align-self:flex-start">applied. i&rsquo;ll message you the moment they reply</span>
            <span class="note">Follow-ups chased for you, too.</span>
          </div>
        </div>

        <ul class="lp-assure">
          <li>{icon_eye_p}<span>You see exactly what sends, before it sends</span></li>
          <li>{icon_check_p}<span>Tailored one at a time, never mass-applied</span></li>
          <li>{icon_doc_p}<span>Found a role yourself? Send us the posting and we&rsquo;ll apply</span></li>
        </ul>
      </div>
    </section>

    <section class="lp-band" id="companies">
      <div class="wrap">
        <div class="lp-band-intro">
          <span class="lbl">For companies</span>
          <h2>Hiring? We&rsquo;ve already interviewed the pool.</h2>
          <p>Tell us the role and the bar, then consider it handled. White glove the whole way:
            we reach the engineers you want, vet every one ourselves, and hand you introductions
            on your calendar.</p>
        </div>

        <div class="lp-stats">
          <div><b>1,500+</b><span class="lbl">Engineers, pre-interviewed</span></div>
          <div><b>$0</b><span class="lbl">Until you hire &middot; success fee only</span></div>
        </div>

        <div class="lp-steps">
          <button type="button" class="lp-step" data-open="lp-hire" style="animation-delay:.05s">
            <span class="lbl">Step 1 &middot; Reach</span>
            <h3>We reach the exact engineers you want</h3>
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
            <p>Named lists, message-first. Engineers who ignore InMail answer us.</p>
          </button>

          <button type="button" class="lp-step" data-open="lp-hire" style="animation-delay:.15s">
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
          </button>

          <button type="button" class="lp-step" data-open="lp-hire" style="animation-delay:.25s">
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
          </button>
        </div>

        <div class="lp-funnel">
          <div class="lp-funnel-top lbl"><span>Everyone who could do the job</span>
            <span class="hit">Five reach your calendar</span></div>
          <div class="lp-bars" aria-hidden="true">{bars}</div>
          <div class="lp-funnel-foot"><span>1,500 profiles reviewed per search</span>
            <span aria-hidden="true">&rarr;</span>
            <span style="color:var(--band-acc)">5 introductions, with our read on each</span></div>
        </div>

        <div class="lp-booking">
          <div class="t"><b>Grab 20 minutes with us.</b>
            <span>Bring the role. We&rsquo;ll walk you through the pool and show you what our read
              looks like.</span></div>
          <div class="a">
            <button type="button" class="lp-btn" data-open="lp-hire">Book on Calendly</button>
            <small>calendly.com/goforay/intro &middot; 20 min</small>
          </div>
        </div>
      </div>
    </section>

    <section class="lp-closer">
      <div class="wrap">
        <h2>Foray into your <em class="mark-hl">next role</em>.</h2>
        <div class="acts">
          <button type="button" class="lp-btn" data-open="lp-text">Message Foray</button>
          <button type="button" class="lp-btn ghost" data-open="lp-hire">Hiring? Book a call</button>
        </div>
      </div>
    </section>
  </main>

  <footer class="lp-foot">
    <div class="wrap">
      <div class="lp-fcols">
        <div>
          <span class="lp-logo" aria-hidden="true">{logomark}Foray</span>
          <p style="color:var(--muted); margin-top:16px; max-width:30ch">Your autonomous recruiting agent.</p>
        </div>
        <div><h4>Engineers</h4><ul>
          <li><button type="button" data-open="lp-text">Message Foray</button></li>
          <li><button type="button" data-open="lp-call">Request a call</button></li>
          <li><button type="button" data-open="lp-email">apply@goforay.io</button></li>
        </ul></div>
        <div><h4>Hiring</h4><ul>
          <li><button type="button" data-open="lp-hire">Book 20 minutes</button></li>
        </ul></div>
        <div><h4>Contact</h4><ul>
          <li><a href="mailto:{email}">{email}</a></li>
          <li style="color:var(--muted)">San Francisco, CA</li>
        </ul></div>
      </div>
      <div class="lp-fbot lbl">
        <span>&copy; 2026 Foray</span>
        <span>Msg &amp; data rates may apply &middot; Reply STOP to opt out</span>
        <span>Built in San Francisco</span>
      </div>
    </div>
  </footer>

  <audio id="lp-voice" preload="none" src="/foray-voice.mp3"></audio>
  <span hidden id="lp-thumb-src">{icon_thumb_w}</span>
  <span hidden id="lp-stripe-src">{stripe_badge}</span>

  <dialog class="lp-modal" id="lp-text">
    <div class="box">
      <button type="button" class="x" data-close aria-label="Close">{icon_x_i}</button>
      <span class="lbl" style="color:var(--primary)">Message us</span>
      <h3>One message starts it.</h3>
      <span class="big">(628) 386-5454</span><p style="margin-top:-8px">Text that number, or start a thread right here. Both reach the same place.</p>
      <p>Send anything: your LinkedIn, a resume, or a posting you found and want us to apply to.
        A real person reviews every match, and we reply in minutes.</p>
      <span class="lp-free" style="align-self:flex-start">10 applications, free</span>
      <div class="acts">
        <button type="button" class="lp-btn" data-chat>Open the chat</button>
        <button type="button" class="lp-btn ghost" data-close>Got it</button>
      </div>
    </div>
  </dialog>

  <dialog class="lp-modal" id="lp-call">
    <div class="box">
      <button type="button" class="x" data-close aria-label="Close">{icon_x_i}</button>
      <span class="lbl" style="color:var(--primary)">Get a call</span>
      <h3>Foray calls you.</h3>
      <p>Ask for a call in the thread and Foray rings you back, usually within minutes.</p>
      <p>That&rsquo;s the real voice below. On the call Foray asks what roles you&rsquo;d like to do,
        your stack, comp, and where you want to work. Three minutes. Then we find roles that fit
        and send them straight back to you.</p>
      <div class="acts">
        <button type="button" class="lp-btn ghost" data-hear id="lp-hear">{icon_speaker} Hear Foray</button>
        <button type="button" class="lp-btn" data-chat>Ask for a call</button>
      </div>
    </div>
  </dialog>

  <dialog class="lp-modal" id="lp-email">
    <div class="box">
      <button type="button" class="x" data-close aria-label="Close">{icon_x_i}</button>
      <span class="lbl" style="color:var(--primary)">Email us</span>
      <h3>Forward it. We handle it.</h3>
      <span class="big">apply@goforay.io</span>
      <p>Send your resume, or forward a job description you found. We fill out the application for
        you and show it to you before it goes out.</p>
      <div class="acts">
        <a class="lp-btn" href="mailto:apply@goforay.io">Open your mail app</a>
        <button type="button" class="lp-btn ghost" data-close>Got it</button>
      </div>
    </div>
  </dialog>

  <dialog class="lp-modal" id="lp-hire">
    <div class="box">
      <button type="button" class="x" data-close aria-label="Close">{icon_x_i}</button>
      <span class="lbl" style="color:var(--accent-deep)">For companies</span>
      <h3>Grab 20 minutes with us.</h3>
      <div class="lp-month">
        <div class="hdr"><b>September</b><span>Pick a day</span></div>
        <div class="lp-days">
          <span>8</span><span>9</span><span>10</span><span class="sel">11</span>
          <span>12</span><span>15</span><span>16</span>
        </div>
        <div class="lp-times"><span>10:00</span><span class="sel">2:30</span><span>4:00</span></div>
      </div>
      <p>Five tailored candidates, our read on each. You pay only when you hire.</p>
      <div class="acts">
        <a class="lp-btn" href="https://calendly.com/goforay/intro" target="_blank" rel="noopener">Book on Calendly</a>
        <button type="button" class="lp-btn ghost" data-close>Close</button>
      </div>
    </div>
  </dialog>

</div>
""".format(
    logomark=LOGOMARK,
    email="{email}",
    drift_a=_drift(DRIFT_A),
    drift_b=_drift(DRIFT_B),
    bars=_bars(),
    chips="".join([
        chip("anthropic", "Anthropic", "0"),
        chip("openai", "OpenAI", ".2"),
        chip("googlegemini", "Google DeepMind", ".4"),
        chip("meta", "Meta", ".6"),
        chip("stripe", "Stripe", ".8"),
    ]),
    stripe_badge=mark("stripe", 11),
    wave="".join('<i style="height:%dpx; animation-delay:%.2fs"></i>' % (h, i * 0.12)
                 for i, h in enumerate([22, 30, 16, 26, 14, 24, 18])),
    icon_down=_svg(I["down"], 13),
    icon_up_w=_svg(I["up"], 15, "#fff"),
    icon_chat_w=_svg(I["chat"], 20, "#fff"),
    icon_chat_p=_svg(I["chat"], 20, "var(--primary)"),
    icon_phone_p=_svg(I["phone"], 20, "var(--primary)"),
    icon_mail_p=_svg(I["mail"], 20, "var(--primary)"),
    icon_team_a=_svg(I["team"], 20, "var(--accent-deep)"),
    icon_arrow_w=_svg(I["arrow"], 18, "#fff"),
    icon_arrow_a=_svg(I["arrow"], 18, "var(--accent-deep)"),
    icon_arrow_sm=_svg('<path d="m9 6 6 6-6 6"/>', 16, "var(--primary)"),
    icon_user_w=_svg(I["user"], 18, "#fff"),
    icon_check_p=_svg(I["check"], 15, "var(--primary)"),
    icon_check_g=_svg(I["check"], 14, "var(--band-acc)"),
    icon_check_dark=_svg(I["check"], 12, "var(--band)", extra=' stroke-width="3"'),
    icon_x_m=_svg(I["x"], 14, "rgba(255,255,255,.5)"),
    icon_x_i=_svg(I["x"], 14, "var(--ink)"),
    icon_doc_p=_svg(I["doc"], 12, "var(--primary)"),
    icon_pen_w=_svg(I["pen"], 14, "#fff"),
    icon_eye_p=_svg(I["eye"], 16, "var(--primary)"),
    icon_bolt_w=_svg(I["bolt"], 17, "#fff"),
    icon_bolt_a=_svg(I["bolt"], 11, "var(--accent-deep)"),
    icon_send_w=_svg(I["send"], 11, "#fff"),
    icon_speaker=_svg(I["speaker"], 14),
    icon_thumb_w=_svg(I["thumb"], 12, "#fff"),
    icon_flow=('<svg width="40" height="24" viewBox="0 0 40 24" fill="none" stroke="currentColor" '
               'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
               '<path d="M2 12h30"/><path d="m29 6 8 6-8 6" stroke-dasharray="0"/></svg>'),
)
