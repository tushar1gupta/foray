#!/usr/bin/env python3
"""The shared shell: palette, components and chrome for every page.

This file used to be the candidate landing page and is still named for it. It
is now only the design system -- tokens, the card and button classes, the icon
set, the ticker, the top bar and the footer -- imported by company.py,
candidate.py and legal pages alike. The candidate page itself is parked in
src/parked/candidates.py and is no longer generated.

The palette is "First light", dawn purple. Every page wears it; there is no
second shell left to reconcile it with.

Brand marks for the matched companies are read from ``src/logos`` at build time
and inlined, so the page makes no third-party requests. They identify the
company whose role is being shown; they are not endorsements and must not be
used as a "trusted by" wall.

Two copy rules, both deliberate:

1. Nothing here describes software. Foray presents as a recruiting agency, so
   the footer tagline, the ticker and the calls to action all talk about
   searches and introductions, never about an agent or automation. The AI
   disclosures in legal.py are a separate matter -- those describe what actually
   happens and must stay accurate.
2. Nothing here names a function. We may recruit for any of them, so the copy
   says roles, candidates and people -- never "engineers", which reads as the
   only thing we do and dates the page the first time we run a GTM search.
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
.lp :focus-visible{outline:2px solid var(--primary); outline-offset:3px}
/* ticker + header */
.lp-ticker{background:var(--primary); color:#fff; text-align:center; padding:9px var(--gut)}
/* Full bleed on the outside so the background spans the window,layout on the
   inside so it still lines up with the rest of the page. Sticky needs the
   former: a max-width bar lets content scroll past on either side of it. */
.lp-head{position:sticky; top:0; z-index:20; border-bottom:1px solid var(--line);
  background:rgba(250,248,252,.86);
  -webkit-backdrop-filter:saturate(180%) blur(12px); backdrop-filter:saturate(180%) blur(12px)}

@supports not ((backdrop-filter:blur(1px)) or (-webkit-backdrop-filter:blur(1px))){
.lp-head{background:var(--bg)}}
.lp-head-in{
  display:flex; align-items:center; gap:16px; flex-wrap:wrap;
  max-width:var(--wrap); margin:0 auto; padding:20px var(--gut);
}
/* an in-page link would otherwise land its target underneath the bar */
html{scroll-padding-top:100px}
.lp-logo{display:inline-flex; align-items:center; gap:12px; font-weight:600; font-size:19px;
  letter-spacing:.2em; text-transform:uppercase; line-height:1}
.lp-logo b{display:grid; grid-template-columns:repeat(2,5px); gap:2.5px}
.lp-head .lp-logo{font-size:24px; gap:14px}
.lp-head .lp-logo b{grid-template-columns:repeat(2,7px); gap:3px}
.lp-head .lp-logo i{width:7px; height:7px; border-radius:1.5px}
.lp-logo i{width:5px; height:5px; background:var(--primary); border-radius:1px}
.lp-logo i:nth-child(2){opacity:.5}
.lp-logo i:nth-child(3){opacity:.4}
/* The audience switch: two anchors dressed as a segmented control,so it needs
   no script,survives a right-click into a new tab{display:flex; margin:0 auto; padding:3px; gap:2px; border-radius:999px;
  background:var(--tint2); border:1px solid var(--line)}

@media(max-width:640px){
html{scroll-padding-top:76px}
.lp-head-in{padding:12px var(--gut); gap:10px}
.lp-head .lp-logo{font-size:18px; gap:10px}
.lp-head .lp-logo b{grid-template-columns:repeat(2,5px); gap:2.5px}
.lp-head .lp-logo i{width:5px; height:5px}
.lp-head-in > .lp-btn{display:none}}
/* a quiet route to the other side of the business,for anyone who arrived on
   the wrong one */
.lp-crosslink{padding:clamp(30px,4vw,48px) var(--gut) clamp(40px,5vw,60px)}
.lp-crosslink .wrap{max-width:var(--wrap); margin:0 auto}
.lp-crosslink a{display:flex; align-items:center; gap:18px; justify-content:space-between;
  padding:22px 26px; border:1px solid var(--primary2); border-radius:16px;
  background:var(--tint); color:var(--ink);
  transition:border-color .18s ease, transform .18s ease, box-shadow .18s ease}
.lp-crosslink a:hover{border-color:var(--primary); transform:translateY(-2px);
  box-shadow:0 10px 26px rgba(106,80,200,.18)}
.lp-crosslink b{font-weight:600}
.lp-crosslink .go{color:var(--primary); font-size:20px}

@media(max-width:900px){
.lp-head .lp-btn{margin-left:auto}}
/* buttons */
.lp-btn{display:inline-flex; align-items:center; justify-content:center; gap:8px; cursor:pointer;
  font:inherit; font-size:11.5px; font-weight:600; letter-spacing:.15em; text-transform:uppercase;
  padding:14px 24px; border:0; border-radius:999px; background:var(--primary); color:#fff;
  transition:transform .18s,box-shadow .18s,background .18s}
.lp-btn:hover{transform:translateY(-2px); box-shadow:0 10px 24px rgba(42,33,64,.22)}
.lp-btn.ghost{background:transparent; color:var(--ink); border:1px solid var(--line2)}
.lp-btn.ghost:hover{border-color:var(--primary); color:var(--primary)}
/* `.lp a{color:inherit}
` above is 0,1,1 and beats `.lp-btn` at 0,1,0,so an
   anchor wearing the button class renders ink on purple. Name both. */
.lp a.lp-btn{color:#fff}
.lp a.lp-btn.ghost{color:var(--ink)}
.lp a.lp-btn.ghost:hover{color:var(--primary)}
/* Four rows spread down the panel,alternating direction{top:8%; animation:lp-left 34s linear infinite; opacity:.85}

@keyframes lp-left{from{transform:translateX(0)}to{transform:translateX(-50%)}}
/* A tapback sits on the far corner of the bubble it belongs to{margin-top:18px}

@keyframes lp-rise{from{opacity:0; transform:translateY(10px)}to{opacity:1; transform:none}}
/* the job card that reads as a link preview */
/* Both of these are spans holding block-level children. Left inline they grow a
   line-height strut above the first child,which opens an empty band at the top
   of the card and,worse{position:relative; display:block; margin-top:6px}
/* visible to a screen reader,to nothing else. The hidden attribute would
   take it out of the accessibility tree as well{position:absolute; width:1px; height:1px; margin:-1px; padding:0; border:0;
  overflow:hidden; clip:rect(0 0 0 0); clip-path:inset(50%); white-space:nowrap}
/* One step per character,and a target the width of the actual string --
   a generous target reaches full width in the first step or two,which reads
   as a jump rather than typing{animation-name:lp-t1; animation-timing-function:steps(8)}

@keyframes lp-t1{0%,6%{max-width:0}16%,100%{max-width:9ch}}
/* The nib sits inline directly after the text it is writing,so it travels
   with the characters instead of hovering at the edge of the field. One per
   row{display:inline-flex; align-items:center; gap:5px; vertical-align:middle;
  margin-left:6px; opacity:0; animation-duration:7s; animation-timing-function:ease;
  animation-iteration-count:infinite; animation-fill-mode:both}
/* companies */
.lp-band{background:var(--band); color:#fff}
.lp-band h2{color:#fff; max-width:22ch}
.lp-band .wrap{padding-top:clamp(56px,7vw,88px); padding-bottom:clamp(56px,7vw,88px)}
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
   panel and warmed,rather than sharing the flat treatment of the two nils. */
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
.lp-foot{padding:clamp(40px,5vw,56px) 0 40px}
.lp-fcols{display:grid; grid-template-columns:1.4fr repeat(3,1fr); gap:32px}

@media(max-width:820px){
.lp-fcols{grid-template-columns:1fr 1fr}}
.lp-fcols h4{color:var(--muted); margin:0 0 16px; font-size:11px; font-weight:700;
  letter-spacing:.16em; text-transform:uppercase}
.lp-fcols li{padding:5px 0}
.lp-fcols button{background:none; border:0; padding:0; font:inherit; color:inherit; cursor:pointer; text-align:left}
.lp-fcols button:hover{color:var(--primary)}
/* the legal pages carry links here where the landing page carries buttons */
.lp-fcols a:hover{color:var(--primary)}
.lp-fbot{display:flex; flex-wrap:wrap; gap:14px 30px; justify-content:space-between; color:var(--muted);
  border-top:1px solid var(--line); margin-top:clamp(32px,4vw,48px); padding-top:22px}
/* the legal pages: the only long-form prose on the site,so it gets a measure
   that is comfortable to read rather than the full width of the page */
.lp-legal{max-width:var(--wrap); margin:0 auto; padding:clamp(34px,5vw,56px) var(--gut) clamp(20px,3vw,32px)}
.lp-legal h1{font-size:clamp(30px,4.2vw,46px); margin:0 0 4px}
.lp-legal .body{max-width:72ch}
.lp-legal h2{font-size:clamp(18px,1.7vw,22px); margin:40px 0 10px}
.lp-legal h3{font-size:1.04em; margin:22px 0 6px}
.lp-legal p,.lp-legal li{color:var(--muted); margin:10px 0; line-height:1.68}
.lp-legal ul{margin:10px 0 12px 20px; list-style:disc}
.lp-legal li{padding-left:4px}
.lp-legal li::marker{color:var(--primary2)}
.lp-legal a{color:var(--primary); text-decoration:underline; text-underline-offset:2px}
.lp-legal strong{color:var(--ink); font-weight:600}
.lp-legal code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:.88em;
  background:var(--tint2); border:1px solid var(--line); border-radius:5px; padding:1px 5px}
.lp-legal .meta{color:var(--muted); margin-bottom:26px}
.lp-legal table{width:100%; border-collapse:collapse; margin:16px 0; font-size:14px}
.lp-legal th,.lp-legal td{text-align:left; padding:9px 12px; border-bottom:1px solid var(--line);
  vertical-align:top}
.lp-legal th{color:var(--ink); font-weight:600}
.lp-legal td{color:var(--muted)}
/* The hire dialog carries the real scheduler,which wants more width than a
   dialog sized for three form fields{max-width:min(720px,94vw)}
/* ---- waitlist form ---------------------------------------------------- */
.lp [hidden]{display:none}


@media (prefers-reduced-motion:reduce){
.lp *,.lp *::before,.lp *::after{animation-duration:.01ms!important; animation-iteration-count:1!important;
    transition-duration:.01ms!important}
.lp-step{opacity:1!important; transform:none!important}}
"""


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


def head_bar(active):
    """The ticker and top bar every page shares.

    `active` is "home", "candidates" or None. The site sells one thing now --
    recruiting to companies -- so there is no audience switch in the
    bar. The candidate intake is reachable from the footer and from our own
    outreach, not from a toggle that would make the homepage look like it is
    addressing two people at once.
    """
    if active == "candidates":
        note = ("Recruiting for startups &middot; seed through growth "
                "&middot; San Francisco")
        cta = '<a class="lp-btn" href="index.html">For companies</a>'
    else:
        note = ("Now booking searches &middot; five qualified candidates per role "
                "&middot; success fee only")
        cta = '<a class="lp-btn" href="index.html#role">Send us a role</a>'

    return (
        '  <div class="lp-ticker lbl">' + note + '</div>\n\n'
        '  <header class="lp-head">\n'
        '    <div class="lp-head-in">\n'
        '    <a href="index.html" class="lp-logo" aria-label="Foray home">' + LOGOMARK + 'Foray</a>\n'
        '    ' + cta + '\n'
        '    </div>\n'
        '  </header>\n'
    )


def foot(active):
    """The shared footer.

    One column for the people hiring, one for the people we place, and no
    product language: this is a search firm's footer. Deliberately no mailbox --
    every route in is a form or the calendar, both of which reach somebody.
    """
    home = "" if active == "home" else "index.html"
    return (
        '  <footer class="lp-foot">\n'
        '    <div class="wrap">\n'
        '      <div class="lp-fcols">\n'
        '        <div>\n'
        '          <span class="lp-logo" aria-hidden="true">' + LOGOMARK + 'Foray</span>\n'
        '          <p style="color:var(--muted); margin-top:16px; max-width:32ch">'
        'Recruiting for startups, from seed through growth stage.</p>\n'
        '        </div>\n'
        '        <div><h4>Hiring</h4><ul>\n'
        '          <li><a href="' + home + '#role">Send us a role</a></li>\n'
        '          <li><a href="' + home + '#how">How a search runs</a></li>\n'
        '          <li><a href="' + home + '#book">Book 15 minutes</a></li>\n'
        '        </ul></div>\n'
        '        <div><h4>Candidates</h4><ul>\n'
        '          <li><a href="candidates.html">Introduce yourself</a></li>\n'
        '          <li><a href="candidates.html#work">How this works</a></li>\n'
        '        </ul></div>\n'
        '        <div><h4>Foray</h4><ul>\n'
        '          <li style="color:var(--muted)">San Francisco, CA</li>\n'
        '          <li style="color:var(--muted)">GoForay, Co.</li>\n'
        '        </ul></div>\n'
        '      </div>\n'
        '      <div class="lp-fbot lbl">\n'
        '        <span>&copy; 2026 GoForay, Co.</span>\n'
        '        <span><a href="privacy.html">Privacy</a> &middot; '
        '<a href="terms.html">Terms</a></span>\n'
        '        <span>Built in San Francisco</span>\n'
        '      </div>\n'
        '    </div>\n'
        '  </footer>\n'
    )

def legal_shell(h1, prose):
    """A legal page wearing the landing page's chrome.

    Links, not buttons: these pages ship no script, so there is no waitlist
    dialog here to open. Everything points back at the landing page, which is
    where it lives.
    """
    return (
        '<div class="lp">\n\n'
        + head_bar(None)
        + '\n'
        '  <main class="lp-legal">\n'
        '    <h1>' + h1 + '</h1>\n'
        '    <div class="body">\n' + prose + '\n    </div>\n'
        '  </main>\n\n'
        + foot(None)
        + '\n'
        '</div>\n'
    )
