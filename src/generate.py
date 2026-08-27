#!/usr/bin/env python3
"""Builds the Foray site: three pages, a 404, and the hero scene.

Writes index.html, companies.html, engineers.html and 404.html to the repo root.
Run src/configure.py afterwards to stamp the domain and emit the static assets.
"""
import json, pathlib
from scene import field, frames
from landing import CSS as LP_CSS, JS as LP_JS, BODY as LP_BODY

OUT = pathlib.Path(__file__).resolve().parent.parent
OUT.mkdir(parents=True, exist_ok=True)
EMAIL = "contact@goforay.ai"
SCENE = ('<div class="holo" aria-hidden="true"><div class="stage">'
         '<pre class="field" id="field"></pre>'
         '<pre class="walker"></pre><pre class="walker"></pre>'
         '<span class="scan"></span></div></div>')

CSS = r"""
:root{
  --bg:#080D0B;
  --bg2:#0B120F;
  --panel:#050908;
  --text:#E6EDE9;
  --mut:#8DA29B;
  --mint:#5FE4CE;
  --rule:rgba(230,237,233,.10);
  --rule2:rgba(230,237,233,.22);
  --f:"Instrument Sans",system-ui,-apple-system,sans-serif;
  --mono:ui-monospace,"SF Mono",SFMono-Regular,Menlo,Consolas,monospace;
  --gut:clamp(20px,4.4vw,64px);
  --maxw:1320px;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--text);font-family:var(--f);font-weight:400;
  font-size:clamp(15.5px,1vw,17px);line-height:1.6;letter-spacing:-.005em;-webkit-font-smoothing:antialiased}
::selection{background:var(--mint);color:#04100D}
a{color:inherit;text-decoration:none}
:focus-visible{outline:1.5px solid var(--mint);outline-offset:3px}
h1,h2,h3{font-weight:500;letter-spacing:-.032em;margin:0;text-wrap:balance}
h1{font-size:clamp(38px,4.9vw,68px);line-height:1.02}
h1.t2{font-size:clamp(29px,3.5vw,46px);line-height:1.06}
h2{font-size:clamp(27px,3.3vw,44px);line-height:1.06}
h3{font-size:1.12em;letter-spacing:-.018em}
p{margin:0}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 var(--gut)}
.lbl{font-size:11px;font-weight:500;letter-spacing:.16em;text-transform:uppercase;line-height:1.5}
.dim{color:var(--mut)}
.hl{background:var(--mint);color:#04100D;padding:0 .1em;box-decoration-break:clone;
  -webkit-box-decoration-break:clone}

/* ticker + nav */
.ticker{border-bottom:1px solid var(--rule);background:var(--bg)}
.ticker div{display:flex;justify-content:center;gap:10px;padding:9px 0;color:var(--mut);text-align:center}
.ticker s{text-decoration:none;color:var(--rule2)}
header{position:sticky;top:0;z-index:60;background:rgba(8,13,11,.9);backdrop-filter:blur(16px);
  border-bottom:1px solid var(--rule)}
.nav{display:flex;align-items:center;gap:20px;height:72px}
.mark{display:inline-flex;align-items:center;gap:12px;font-weight:600;font-size:20px;
  letter-spacing:.2em;text-transform:uppercase;line-height:1}
header .mark{margin-right:auto}
.mark b{display:grid;grid-template-columns:repeat(2,5px);gap:2.5px}
.mark i{width:5px;height:5px;background:var(--mint);border-radius:1px;opacity:.9}
.mark i:nth-child(2){opacity:.45}
.mark i:nth-child(3){opacity:.35}
nav.links{display:flex;gap:clamp(14px,2vw,28px)}
nav.links a{color:var(--mut);transition:color .18s}
nav.links a:hover,nav.links a.on{color:var(--text)}
.clock{display:flex;gap:10px;color:var(--mut);padding-left:clamp(8px,1.4vw,20px);
  border-left:1px solid var(--rule)}
.clock span{font-variant-numeric:tabular-nums}
.navcta{border:1px solid var(--rule2);border-radius:999px;padding:9px 17px;white-space:nowrap;
  transition:background .18s,color .18s,border-color .18s}
.navcta:hover{background:var(--mint);color:#04100D;border-color:var(--mint)}
@media(max-width:900px){
  .clock{display:none}
  .nav{flex-wrap:wrap;height:auto;padding:13px 0 11px}
  nav.links{order:3;width:100%;border-top:1px solid var(--rule);padding-top:11px;
    justify-content:space-between;gap:8px}
}

/* hero split */
.hero{display:grid;grid-template-columns:1fr 1fr;align-items:stretch;border-bottom:1px solid var(--rule)}
.hero-l{display:flex;flex-direction:column;justify-content:center;min-height:min(80vh,780px);padding:0}
.hcopy{padding:clamp(40px,5vw,72px) clamp(28px,4vw,56px) 0 var(--gut)}
.hcopy .sub{max-width:42ch}
h1 .ln{display:block;overflow:hidden}
h1 .ln span{display:block;transform:translateY(104%);animation:rise .9s cubic-bezier(.19,1,.22,1) forwards}
h1 .ln:nth-child(2) span{animation-delay:.09s}
@keyframes rise{to{transform:translateY(0)}}
.sub{margin-top:24px;color:var(--mut);font-size:1.1em;max-width:44ch;opacity:0;
  animation:fade .8s .42s ease forwards}
@keyframes fade{to{opacity:1}}

/* ask box, after Inception's prompt field */
.ask{margin-top:clamp(32px,4.4vw,60px);border-top:1px solid var(--rule);
  border-bottom:1px solid var(--rule);background:var(--bg2);
  display:flex;align-items:center;gap:12px;
  padding:10px clamp(16px,2vw,26px) 10px var(--gut);opacity:0;
  animation:fade .8s .56s ease forwards}
.ask input{flex:1;min-width:0;background:none;border:0;color:var(--text);font:inherit;
  padding:17px 0;font-size:1.06em;letter-spacing:-.008em}
.ask input::placeholder{color:var(--mut)}
.ask input:focus{outline:none}
.go{flex:0 0 auto;width:46px;height:46px;border-radius:50%;border:0;background:var(--text);
  color:#04100D;cursor:pointer;display:grid;place-items:center;transition:background .18s,transform .18s}
.go:hover{background:var(--mint);transform:translateY(-1px)}
.go svg{width:17px;height:17px}
.sugg{list-style:none;margin:0;padding:0;opacity:0;animation:fade .8s .68s ease forwards}
.sugg li{border-bottom:1px solid var(--rule)}
.sugg button{width:100%;display:flex;align-items:center;gap:16px;background:none;border:0;
  color:var(--text);font:inherit;font-size:1.04em;text-align:left;cursor:pointer;
  padding:clamp(19px,2.2vw,26px) clamp(16px,2vw,26px) clamp(19px,2.2vw,26px) var(--gut);
  transition:color .18s,background .18s}
.sugg button:hover{color:var(--mint);background:var(--bg2)}
.sugg svg{flex:0 0 auto;width:18px;height:18px;stroke:var(--mut);fill:none;stroke-width:1.4}
.sugg button:hover svg{stroke:var(--mint)}

/* the scene: engineers walking toward a company */
.hero-r{position:relative;background:var(--panel);overflow:hidden;border-left:1px solid var(--rule);
  display:grid;place-items:center;contain:paint}
.holo{position:relative;width:100%;height:100%;display:grid;place-items:center;overflow:hidden}
.stage{position:relative;display:inline-block;margin-left:6%;
  animation:sway 19s ease-in-out infinite alternate}
.field,.walker{font-family:var(--mono);font-size:max(.83vw,1.32vh);line-height:1;letter-spacing:0;
  margin:0;white-space:pre;user-select:none}
.field{color:var(--mut);animation:wake 1.6s .2s ease both}
.walker{position:absolute;left:0;bottom:7em;color:var(--mint);opacity:0;
  text-shadow:0 0 .42em rgba(95,228,206,.5);animation:travel 21s linear infinite}
.walker:nth-of-type(2){animation-delay:-10.5s}
@keyframes travel{
  0%{transform:translateX(3em);opacity:0}
  9%{opacity:.34}
  58%{opacity:.68}
  90%{transform:translateX(51.3em);opacity:1}
  100%{transform:translateX(54em);opacity:0}
}
@keyframes sway{from{transform:translateX(-9px)}to{transform:translateX(9px)}}
@keyframes wake{from{opacity:0}to{opacity:1}}
.field .a0{color:transparent}
.field .a1{color:rgba(141,162,155,.13)}
.field .a2{color:rgba(141,162,155,.22)}
.field .a3{color:rgba(141,162,155,.36)}
.field .a4{color:rgba(160,190,182,.55)}
.field .a5{color:rgba(95,228,206,.50)}
.field .a6{color:rgba(95,228,206,.74)}
.field .a7{color:rgba(140,243,226,.92)}
.field .win{transition:color .5s ease}
.field .win.on{color:#B9FFF2}
.field .win.kept{color:#DDFFF6;text-shadow:0 0 .34em rgba(140,243,226,.75)}
.scan{position:absolute;left:0;right:0;height:26%;pointer-events:none;
  background:linear-gradient(180deg,transparent,rgba(95,228,206,.05) 45%,transparent);
  animation:scan 9s linear infinite}
@keyframes scan{from{top:-30%}to{top:104%}}
@media(max-width:960px){
  .hero{grid-template-columns:1fr}
  .hero-l{min-height:0;padding-right:0}
  .hero-r{border-left:0;border-top:1px solid var(--rule);height:70vw;max-height:540px}
  .field,.walker{font-size:1.62vw}
  .stage{margin-left:4%}
}

/* candidate / company toggle */
.tabs{display:inline-flex;gap:2px;padding:3px;border:1px solid var(--rule);border-radius:999px;
  background:var(--bg2);margin-top:clamp(26px,3.4vw,40px)}
.tabs button{border:0;background:none;color:var(--mut);font:inherit;font-size:11px;font-weight:500;
  letter-spacing:.16em;text-transform:uppercase;padding:11px 22px;border-radius:999px;cursor:pointer;
  transition:background .2s,color .2s}
.tabs button[aria-selected="true"]{background:var(--mint);color:#04100D}
.tabs button:hover[aria-selected="false"]{color:var(--text)}
.panel[hidden]{display:none}
.panel .note{margin-top:22px;color:var(--mut);max-width:52ch}

/* onboarding forms */
.form{margin-top:clamp(30px,4vw,48px);display:grid;grid-template-columns:repeat(2,1fr);
  gap:1px;background:var(--rule)}
.fld{background:var(--bg);padding:18px clamp(18px,2vw,24px) 20px;display:flex;flex-direction:column;gap:9px}
.fld.wide{grid-column:1/-1}
.fld label{color:var(--mut);font-size:10.5px;font-weight:500;letter-spacing:.15em;text-transform:uppercase}
.fld input,.fld textarea,.fld select{background:none;border:0;border-bottom:1px solid var(--rule);
  color:var(--text);font:inherit;padding:8px 0;width:100%}
.fld textarea{resize:vertical;min-height:88px;line-height:1.5}
.fld select{appearance:none;cursor:pointer}
.fld select option{background:var(--bg2);color:var(--text)}
.fld input:focus,.fld textarea:focus,.fld select:focus{outline:none;border-bottom-color:var(--mint)}
.fld input.prefilled,.fld textarea.prefilled{border-bottom-color:var(--mint);color:var(--text)}
.fld.prefilled-card{background:var(--bg2);animation:landed 2.4s ease both}
@keyframes landed{0%,55%{box-shadow:inset 2px 0 0 var(--mint)}100%{box-shadow:inset 2px 0 0 transparent}}
.fld input::placeholder,.fld textarea::placeholder{color:rgba(141,162,155,.55)}
.formfoot{display:flex;flex-wrap:wrap;align-items:center;gap:16px;margin-top:24px}
.formfoot p{color:var(--mut);font-size:.92em;max-width:44ch}
@media(max-width:760px){.form{grid-template-columns:1fr}}

/* sections */
.sec{padding:clamp(58px,7vw,104px) 0;border-top:1px solid var(--rule)}
.sec.first{border-top:0}
.head{display:grid;grid-template-columns:170px 1fr;gap:clamp(18px,4vw,52px);align-items:start}
.lede{max-width:46ch;margin-top:18px;color:var(--mut);font-size:1.05em}
@media(max-width:760px){.head{grid-template-columns:1fr;gap:12px}}
.btn{display:inline-block;font-size:11.5px;font-weight:500;letter-spacing:.15em;text-transform:uppercase;
  padding:14px 24px;border-radius:999px;background:var(--text);color:#04100D;
  transition:transform .18s,background .18s}
.btn:hover{background:var(--mint);transform:translateY(-2px)}
.btn.ghost{background:transparent;color:var(--mut);border:1px solid var(--rule2)}
.btn.ghost:hover{color:var(--mint);border-color:var(--mint);background:transparent}
.acts{display:flex;flex-wrap:wrap;gap:12px;margin-top:30px}

/* numbered steps */
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--rule);
  margin-top:clamp(32px,4vw,52px)}
.stp{background:var(--bg);padding:clamp(24px,2.6vw,34px)}
.stp .no{display:flex;align-items:baseline;gap:11px;color:var(--mint);margin-bottom:18px}
.stp .no b{font-weight:500;font-size:11px;letter-spacing:.16em}
.stp p{color:var(--mut);margin-top:10px}
@media(max-width:860px){.steps{grid-template-columns:1fr}}

/* screen bar */
.screen{margin-top:clamp(32px,4vw,52px);border-top:1px solid var(--rule);padding-top:20px}
.screen-top{display:flex;justify-content:space-between;gap:16px;color:var(--mut)}
.ticks{display:flex;align-items:flex-end;gap:2px;height:100px;margin-top:18px}
.tick{flex:1 1 auto;min-width:1px;background:var(--mut);opacity:.26;transform-origin:bottom;
  transform:scaleY(0);animation:grow .5s cubic-bezier(.19,1,.22,1) forwards}
@keyframes grow{to{transform:scaleY(1)}}
.tick.hit{opacity:1;background:var(--mint);box-shadow:0 0 12px rgba(95,228,206,.7);cursor:pointer}
.ticks:hover .tick:not(.hit){opacity:.12}
.readout{font-size:12px;color:var(--mint);border-top:1px solid var(--rule);margin-top:13px;
  padding-top:12px;min-height:3em}
.readout.idle{color:var(--mut)}
@media(max-width:720px){.ticks{height:76px}}

/* two-up cells */
.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:1px;background:var(--rule);
  margin-top:clamp(32px,4vw,52px)}
.cell{background:var(--bg);padding:clamp(24px,2.6vw,34px)}
.cell .n{display:block;color:var(--mint);font-size:11px;font-weight:500;letter-spacing:.16em;
  text-transform:uppercase;margin-bottom:14px}
.cell p{color:var(--mut);margin-top:10px;max-width:44ch}
.cell ul{list-style:none;margin:16px 0 0;padding:0}
.cell li{padding:10px 0;border-top:1px solid var(--rule);color:var(--mut);display:flex;gap:12px}
.cell li::before{content:"";flex:0 0 4px;height:4px;background:var(--mint);border-radius:50%;
  margin-top:.62em}
@media(max-width:820px){.grid{grid-template-columns:1fr}}

/* table */
.tbl{margin-top:clamp(32px,4vw,52px);width:100%;border-collapse:collapse}
.tbl th{font-size:10.5px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:var(--mut);
  text-align:left;padding:0 16px 12px 0;border-bottom:1px solid var(--rule2)}
.tbl td{padding:18px 16px 18px 0;border-bottom:1px solid var(--rule);vertical-align:top;color:var(--mut)}
.tbl td.k{color:var(--text);font-weight:500;letter-spacing:-.018em;width:30%}
.tbl td.w{white-space:nowrap;width:14%;color:var(--mint)}
.tbl tbody tr{transition:background .18s}
.tbl tbody tr:hover{background:var(--bg2)}
@media(max-width:760px){
  .tbl thead{display:none}
  .tbl tr{display:block;padding:18px 0;border-bottom:1px solid var(--rule)}
  .tbl td{display:block;border:0;padding:0;width:auto}
  .tbl td.k{font-size:1.08em;margin-bottom:5px}
  .tbl td.w{margin-bottom:6px;font-size:11px;letter-spacing:.14em;text-transform:uppercase}
}

/* quotes */
.quotes{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--rule);
  margin-top:clamp(32px,4vw,52px)}
.q{background:var(--bg);padding:clamp(24px,2.6vw,32px);display:flex;flex-direction:column;
  justify-content:space-between}
.q p{font-size:1.03em;letter-spacing:-.014em}
.q cite{display:block;margin-top:22px;padding-top:15px;border-top:1px solid var(--rule);
  color:var(--mut);font-style:normal;font-size:10.5px;font-weight:500;letter-spacing:.14em;
  text-transform:uppercase;line-height:1.5}
@media(max-width:880px){.quotes{grid-template-columns:1fr}}

/* band */
.band{padding:clamp(56px,7vw,100px) 0;border-top:1px solid var(--rule);background:var(--bg2)}
.band h2{max-width:26ch}
.band h2 i{font-style:normal;color:var(--mint)}

/* closer + footer */
.closer{padding:clamp(66px,8.5vw,118px) 0;border-top:1px solid var(--rule)}
.closer h2{margin-top:18px;max-width:20ch}
footer{border-top:1px solid var(--rule);padding:clamp(40px,5vw,64px) 0 40px}
.fcols{display:grid;grid-template-columns:1.4fr repeat(3,1fr);gap:32px}
.fcols h4{color:var(--mut);font-size:11px;font-weight:500;letter-spacing:.16em;text-transform:uppercase;
  margin:0 0 16px}
.fcols ul{list-style:none;margin:0;padding:0;display:grid;gap:10px}
.fcols a:hover{color:var(--mint)}
.fbrand p{color:var(--mut);margin-top:16px;max-width:30ch;font-size:.94em}
.fbot{display:flex;flex-wrap:wrap;gap:14px 30px;justify-content:space-between;color:var(--mut);
  border-top:1px solid var(--rule);margin-top:clamp(36px,4.5vw,56px);padding-top:22px}
@media(max-width:820px){.fcols{grid-template-columns:1fr 1fr}}

.rv{opacity:0;transform:translateY(12px);
  transition:opacity .7s cubic-bezier(.19,1,.22,1),transform .7s cubic-bezier(.19,1,.22,1)}
.rv.in{opacity:1;transform:none}

@media(prefers-reduced-motion:reduce){
  *{animation-duration:.01ms!important;animation-delay:0s!important;transition-duration:.01ms!important}
  .rv{opacity:1;transform:none}
  h1 .ln span{transform:none}
  .sub,.ask,.sugg,.field{opacity:1}
  .tick{transform:scaleY(1)}
  .stage{transform:none}
  .walker{opacity:.75;transform:translateX(20em)}
  .walker:nth-of-type(2){opacity:1;transform:translateX(45em)}
  .scan{display:none}
}
"""

JS = r"""
(function(){
  /* reveals */
  var rv=document.querySelectorAll('.rv');
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){
      es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});
    },{rootMargin:'0px 0px -10% 0px',threshold:.05});
    for(var i=0;i<rv.length;i++){io.observe(rv[i]);}
  }else{for(var j=0;j<rv.length;j++){rv[j].classList.add('in');}}

  /* San Francisco clock */
  var clk=document.getElementById('clk');
  if(clk){
    var tick=function(){
      try{
        clk.textContent=new Intl.DateTimeFormat('en-US',{timeZone:'America/Los_Angeles',
          hour:'2-digit',minute:'2-digit',hour12:false}).format(new Date());
      }catch(e){clk.textContent='--:--';}
    };
    tick();setInterval(tick,20000);
  }

  /* ask box -> the company onboarding page, carrying what they typed */
  var send=function(text){
    var t=(text||'').trim();
    if(!t){return;}
    window.location.href='companies.html?role='+encodeURIComponent(t);
  };
  var q=document.getElementById('q');
  var go=document.getElementById('go');
  if(q&&go){
    go.addEventListener('click',function(){send(q.value);});
    q.addEventListener('keydown',function(e){if(e.key==='Enter'){send(q.value);}});
    var sg=document.querySelectorAll('.sugg button');
    for(var k=0;k<sg.length;k++){
      sg[k].addEventListener('click',function(){
        q.value=this.getAttribute('data-q');q.focus();
      });
    }
  }


  /* the static field is deterministic, so it is generated here instead of shipped as markup */
  var fieldEl=document.getElementById('field');
  if(fieldEl){
    var COLS=122,ROWS=64,GROUND=55,B_L=78,B_R=113,B_T=13,DOOR_L=92,DOOR_R=99,DOOR_T=49;
    var GLYPHS="01<>[]{}()/\\|=+-*&%$#@!?;:,.^~_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    var SPARSE=".,:;'`^~-_ ";
    var MID="abcdehknopsuvxyz2345679=+*<>[]{}()/\\|";
    var sd=9;
    var rnd=function(){sd=((Math.imul(sd,1103515245)+12345)&0x7FFFFFFF);return sd/2147483648;};
    var cells=[],r,c,k;
    for(r=0;r<ROWS;r++){cells.push(new Array(COLS));}
    for(r=0;r<ROWS;r++){
      c=0;
      var depth=Math.max(0,(r-8)/(ROWS-8));
      while(c<COLS){
        var run=2+((rnd()*8)|0),lv=rnd()<0.20+0.22*depth?1:0;
        if(lv&&rnd()<0.30){lv=2;}
        var lim=Math.min(run,COLS-c);
        for(k=0;k<lim;k++){
          var ch=lv?GLYPHS.charAt((rnd()*GLYPHS.length)|0):SPARSE.charAt((rnd()*SPARSE.length)|0);
          cells[r][c+k]=[lv,ch,''];
        }
        c+=run;
      }
    }
    for(r=B_T;r<GROUND;r++){for(c=B_L;c<B_R;c++){cells[r][c]=[2,MID.charAt((rnd()*MID.length)|0),''];}}
    for(r=B_T;r<GROUND;r++){cells[r][B_L]=[4,'|',''];cells[r][B_R-1]=[4,'|',''];}
    for(c=B_L;c<B_R;c++){cells[B_T][c]=[4,'=',''];}
    for(r=B_T-5;r<B_T;r++){cells[r][95]=[3,'|',''];}
    cells[B_T-6][95]=[7,'*','win'];
    for(r=B_T+3;r<DOOR_T-1;r+=4){
      for(c=B_L+3;c<B_R-5;c+=6){
        var lit=rnd()<0.22;
        for(k=0;k<3;k++){cells[r][c+k]=lit?[7,'#','win']:[5,'=','win'];}
        for(k=0;k<3;k++){cells[r+1][c+k]=lit?[6,'#','win']:[4,'-','win'];}
      }
    }
    for(r=DOOR_T;r<GROUND;r++){for(c=DOOR_L;c<DOOR_R;c++){cells[r][c]=[6,MID.charAt((rnd()*MID.length)|0),''];}}
    for(r=DOOR_T+1;r<GROUND;r++){for(c=DOOR_L+1;c<DOOR_R-1;c++){cells[r][c]=[7,'#','win'];}}
    for(c=DOOR_L;c<DOOR_R;c++){cells[DOOR_T][c]=[7,'=',''];}
    for(c=DOOR_L-9;c<DOOR_L;c++){
      var fall=(c-(DOOR_L-9))/9;
      if(rnd()<0.25+0.55*fall){cells[GROUND-1][c]=[3+((fall*2)|0),'-',''];}
    }
    for(c=0;c<COLS;c++){cells[GROUND][c]=[4,rnd()<0.75?'=':'-',''];}
    for(r=GROUND+1;r<ROWS;r++){
      for(c=0;c<COLS;c++){
        cells[r][c]=rnd()<0.30?[1,SPARSE.charAt((rnd()*SPARSE.length)|0),'']:[0,' ',''];
      }
    }
    var esc=function(t){return t.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');};
    var out=[];
    for(r=0;r<ROWS;r++){
      var row=[],curL=cells[r][0][0],curK=cells[r][0][2],buf=[];
      for(c=0;c<COLS;c++){
        var cell=cells[r][c];
        if(cell[0]===curL&&cell[2]===curK){buf.push(cell[1]);}
        else{
          row.push('<span class="a'+curL+(curK?' win':'')+'">'+esc(buf.join(''))+'</span>');
          curL=cell[0];curK=cell[2];buf=[cell[1]];
        }
      }
      row.push('<span class="a'+curL+(curK?' win':'')+'">'+esc(buf.join(''))+'</span>');
      out.push(row.join(''));
    }
    fieldEl.innerHTML=out.join('\n');
  }

  /* the scene: cycle walk frames and twinkle a few windows */
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var FRAMES=__FRAMES__;
  var walkers=document.querySelectorAll('.walker');
  if(walkers.length){
    for(var a=0;a<walkers.length;a++){walkers[a].textContent=FRAMES[(a*5)%FRAMES.length];}
    if(!reduce){
      var f=0;
      setInterval(function(){
        f=(f+1)%FRAMES.length;
        for(var b=0;b<walkers.length;b++){
          walkers[b].textContent=FRAMES[(f+b*5)%FRAMES.length];
        }
      },95);
    }
  }
  var wins=document.querySelectorAll('.field .win');
  if(wins.length&&!reduce){
    setInterval(function(){
      for(var n=0;n<3;n++){
        var el=wins[(Math.random()*wins.length)|0];
        if(el){el.classList.toggle('on');}
      }
    },900);
  }

  /* a figure that reaches the door becomes part of the building */
  var wins=Array.prototype.slice.call(document.querySelectorAll('.field .win'));
  var order=[],seedw=77;
  for(var q=0;q<wins.length;q++){order.push(q);}
  for(var q2=order.length-1;q2>0;q2--){
    seedw=(seedw*1103515245+12345)%2147483648;
    var j2=seedw%(q2+1),tmp=order[q2];order[q2]=order[j2];order[j2]=tmp;
  }
  var absorbed=0,CAP=Math.min(26,wins.length);
  for(var wk=0;wk<walkers.length;wk++){
    walkers[wk].addEventListener('animationiteration',function(){
      if(absorbed>=CAP){return;}
      var el=wins[order[absorbed]];
      if(el){el.classList.remove('on');el.classList.add('kept');}
      absorbed++;
    });
  }

  /* candidate / company toggle */
  var tabs=document.querySelectorAll('.tabs button');
  for(var t2=0;t2<tabs.length;t2++){
    tabs[t2].addEventListener('click',function(){
      var name=this.getAttribute('data-panel');
      for(var i2=0;i2<tabs.length;i2++){
        tabs[i2].setAttribute('aria-selected',String(tabs[i2]===this));
      }
      var panels=document.querySelectorAll('.panel');
      for(var p2=0;p2<panels.length;p2++){
        panels[p2].hidden=(panels[p2].getAttribute('data-panel')!==name);
      }
    });
  }

  /* carry the hero input into the form */
  try{
    var qs=new URLSearchParams(window.location.search).get('role');
    if(qs){
      var target=qs.length>90?document.getElementById('c-jd'):document.getElementById('c-role');
      if(target){
        target.value=qs;
        target.classList.add('prefilled');
        var card=target.closest('.fld');
        if(card){card.classList.add('prefilled-card');}
        setTimeout(function(){
          target.scrollIntoView({block:'center',behavior:'smooth'});
        },220);
      }
    }
  }catch(e){}

  /* onboarding forms compose an email, since there is no backend yet */
  var forms=document.querySelectorAll('[data-compose]');
  for(var g2=0;g2<forms.length;g2++){
    (function(root){
      var btn=root.querySelector('[data-send]');
      if(!btn){return;}
      btn.addEventListener('click',function(){
        var parts=[],ok=false;
        var fields=root.querySelectorAll('input,textarea,select');
        for(var i3=0;i3<fields.length;i3++){
          var f=fields[i3],v=(f.value||'').trim();
          if(v){ok=true;parts.push((f.getAttribute('data-label')||f.name||'Field')+': '+v);}
        }
        if(!ok){var first=root.querySelector('input,textarea');if(first){first.focus();}return;}
        window.location.href='mailto:contact@goforay.ai?subject='+
          encodeURIComponent(root.getAttribute('data-compose'))+
          '&body='+encodeURIComponent(parts.join('\n')+'\n\n');
      });
    })(forms[g2]);
  }

  /* screen bar */
  var host=document.getElementById('ticks');
  if(host){
    var out=document.getElementById('readout'),idle=out.textContent;
    var small=window.matchMedia('(max-width:700px)').matches;
    var N=small?66:126,hits=small?[9,21,33,45,57]:[17,39,61,83,105];
    var profiles=[
      'Six years on payments infrastructure. Owned the ledger rewrite. Wants a founding role.',
      'Five years platform at a Series C. Built the deploy path three teams depend on.',
      'Maintainer on a Rust async runtime. Three years at a Series B.',
      'Four years applied ML. Took inference latency down 60 percent on consumer GPUs.',
      'Third engineer at a seed company through Series B. Ready to do it again earlier.'
    ];
    var frag=document.createDocumentFragment(),seed=41;
    var rnd=function(){seed=(seed*1103515245+12345)%2147483648;return seed/2147483648;};
    for(var t=0;t<N;t++){
      var d=document.createElement('div'),hi=hits.indexOf(t);
      if(hi>-1){
        d.className='tick hit';d.style.height='100%';
        d.setAttribute('data-p',profiles[hi]);d.setAttribute('tabindex','0');
        d.setAttribute('role','button');d.setAttribute('aria-label','Introduced profile '+(hi+1));
      }else{
        d.className='tick';d.style.height=(12+rnd()*54).toFixed(1)+'%';
      }
      d.style.animationDelay=(t*7)+'ms';
      frag.appendChild(d);
    }
    host.appendChild(frag);host.removeAttribute('aria-hidden');
    var show=function(e){
      var p=e.target.getAttribute?e.target.getAttribute('data-p'):null;
      if(p){out.textContent=p;out.classList.remove('idle');}
    };
    var clear=function(){out.textContent=idle;out.classList.add('idle');};
    host.addEventListener('mouseover',show);host.addEventListener('mouseleave',clear);
    host.addEventListener('focusin',show);host.addEventListener('focusout',clear);
    host.addEventListener('click',show);
  }
})();
""".replace("__EMAIL__", EMAIL).replace("__FRAMES__", json.dumps(frames(10)))

NAVLINKS = [("companies.html", "Companies"), ("engineers.html", "Engineers")]

ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M12 19V5M5 12l7-7 7 7"/></svg>')

ICONS = {
    "spark": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v6M12 15v6M3 12h6M15 12h6"/></svg>',
    "layers": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 8l8-4 8 4-8 4-8-4z"/><path d="M4 14l8 4 8-4"/></svg>',
    "grad": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 9l9-4 9 4-9 4-9-4z"/><path d="M7 12v4c0 1.7 2.2 3 5 3s5-1.3 5-3v-4"/></svg>',
    "growth": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 19V9M10 19V5M16 19v-7M22 19H2"/></svg>',
}



LANDING_FONTS = ("https://fonts.googleapis.com/css2?"
                 "family=Bricolage+Grotesque:wght@500;600;700"
                 "&family=Schibsted+Grotesk:wght@400;500;600&display=swap")


def landing(title, desc):
    """index.html — its own chrome, its own palette, its own script."""
    body = LP_BODY.replace("{email}", EMAIL)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{LANDING_FONTS}" rel="stylesheet">
<style>{LP_CSS}</style>
</head>
<body>
{body}
<script>{LP_JS}</script>
</body>
</html>
"""

def shell(page, title, desc, body):
    nav = "".join('<a href="%s"%s>%s</a>' % (h, ' class="on"' if h == page else "", t)
                  for h, t in NAVLINKS)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<div class="ticker"><div class="wrap lbl"><s>&mdash;</s>Now booking engineering searches for Q4<s>&mdash;</s></div></div>
<header>
  <div class="wrap nav">
    <a href="index.html" class="mark" aria-label="Foray home"><b><i></i><i></i><i></i><i></i></b>Foray</a>
    <nav class="links lbl" aria-label="Main">{nav}</nav>
    <div class="clock lbl"><span>San Francisco</span><span id="clk">--:--</span></div>
    <a href="companies.html" class="navcta lbl">Start a search</a>
  </div>
</header>
<main>
{body}
</main>
<footer>
  <div class="wrap">
    <div class="fcols">
      <div class="fbrand">
        <span class="mark" aria-hidden="true"><b><i></i><i></i><i></i><i></i></b>Foray</span>
        <p>Early and mid-level engineering search for startups.</p>
      </div>
      <div>
        <h4>Hiring</h4>
        <ul>
          <li><a href="companies.html">Post a role</a></li>
          <li><a href="companies.html#roles">What we search for</a></li>
        </ul>
      </div>
      <div>
        <h4>Engineers</h4>
        <ul>
          <li><a href="engineers.html">Join the pool</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li class="dim">San Francisco, CA</li>
        </ul>
      </div>
    </div>
    <div class="fbot lbl"><span>&copy; 2026 Foray</span><span>Built in San Francisco</span></div>
  </div>
</footer>
<script>{JS}</script>
</body>
</html>
"""


CLOSER = f"""  <section class="closer">
    <div class="wrap">
      <h2 class="rv">Foray Into Your Next Hire.</h2>
      <div class="acts rv">
        <a href="companies.html" class="btn">Post a role</a>
        <a href="engineers.html" class="btn ghost">Join the pool</a>
      </div>
    </div>
  </section>
"""

index_body = f"""  <section class="hero">
    <div class="hero-l">
      <div class="hcopy">
      <h1>
        <span class="ln"><span>We Build Early</span></span>
        <span class="ln"><span><em class="hl">Engineering</em> Teams.</span></span>
      </h1>
      <p class="sub">A recruiting firm for startups making early and mid-level engineering hires, from
        seed through growth stage.</p>
      </div>
      <div class="ask">
        <input id="q" type="text" aria-label="Tell us who you want to hire"
          placeholder="I want to hire a...">
        <button class="go" id="go" type="button" aria-label="Continue">{ARROW}</button>
      </div>
      <ul class="sugg">
        <li><button type="button" data-q="I want to hire a founding engineer at seed.">{ICONS['spark']}Founding engineer, seed</button></li>
        <li><button type="button" data-q="I want to hire a senior backend engineer, Series B.">{ICONS['layers']}Senior backend, Series B</button></li>
        <li><button type="button" data-q="I want to hire an infrastructure lead at growth stage.">{ICONS['growth']}Infrastructure lead, growth</button></li>
        <li><button type="button" data-q="I want to build out an applied ML team, Series C.">{ICONS['grad']}Applied ML team, Series C</button></li>
      </ul>
    </div>
    <div class="hero-r">{SCENE}</div>
  </section>

  <section class="sec">
    <div class="wrap">
      <div class="head rv">
        <p class="lbl dim">How It Works</p>
        <div>
          <h2>Three Steps, Either Side Of The Table.</h2>
          <div class="tabs" role="tablist" aria-label="Choose your side">
            <button type="button" role="tab" data-panel="company" aria-selected="true">Company</button>
            <button type="button" role="tab" data-panel="candidate" aria-selected="false">Candidate</button>
          </div>
        </div>
      </div>

      <div class="panel" data-panel="company">
        <div class="steps rv">
          <div class="stp">
            <p class="no"><b>01</b> Introductory call</p>
            <p>An hour on the role, the stack, and the bar.</p>
          </div>
          <div class="stp">
            <p class="no"><b>02</b> Targeted outreach</p>
            <p>We approach a named list, not a job board.</p>
          </div>
          <div class="stp">
            <p class="no"><b>03</b> Introductions</p>
            <p>Five engineers, with our read on each.</p>
          </div>
        </div>
      </div>

      <div class="panel" data-panel="candidate" hidden>
        <div class="steps rv">
          <div class="stp">
            <p class="no"><b>01</b> Opportunity surfaced</p>
            <p>One role, with the stage, team, and comp band stated.</p>
          </div>
          <div class="stp">
            <p class="no"><b>02</b> Fit assessed</p>
            <p>A senior engineer reads your work and tells you what they saw.</p>
          </div>
          <div class="stp">
            <p class="no"><b>03</b> Introduction</p>
            <p>You meet the founder or the engineer you would work with.</p>
          </div>
        </div>
        <p class="note rv">Timeline, location, visa status, and comp are yours to set. Nothing reaches a
          company without your say.</p>
      </div>
    </div>
  </section>

  <section class="sec">
    <div class="wrap">
      <div class="head rv">
        <p class="lbl dim">The Screen</p>
        <div><h2>Fifteen Hundred Profiles, Five Introductions.</h2></div>
      </div>
      <div class="screen rv">
        <div class="screen-top lbl">
          <span>Everyone who could do the job</span>
          <span>Five reach your calendar</span>
        </div>
        <div class="ticks" id="ticks" aria-hidden="true"></div>
        <p class="readout idle" id="readout">Hover a lit mark to see a profile from a recent search.</p>
      </div>
    </div>
  </section>

  <section class="sec">
    <div class="wrap">
      <div class="head rv">
        <p class="lbl dim">What We Do</p>
        <div><h2>We Specialize In Early And Mid-Level Engineering Hires.</h2></div>
      </div>
      <div class="grid rv">
        <div class="cell">
          <span class="n">Early hires</span>
          <h3>Seed to Series A</h3>
          <p>Founding and first-team engineers who have shipped something end to end with nobody
            checking on them.</p>
        </div>
        <div class="cell">
          <span class="n">Mid-level hires</span>
          <h3>Series B through growth</h3>
          <p>Engineers with three to eight years who have owned a system other teams depended on, and
            want more scope than their title allows.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="sec">
    <div class="wrap">
      <div class="head rv">
        <p class="lbl dim">Clients</p>
        <div><h2>What Founders Say.</h2></div>
      </div>
      <div class="quotes rv">
        <div class="q">
          <p>&ldquo;First introductions landed four days after our call. We had spent two months on the
            same role with another firm and seen nobody worth a second conversation.&rdquo;</p>
          <cite>Founder, seed-stage developer tools</cite>
        </div>
        <div class="q">
          <p>&ldquo;Five profiles, four of them we wanted to meet. That hit rate is the whole value. I
            spent no time filtering.&rdquo;</p>
          <cite>Head of Engineering, Series B fintech</cite>
        </div>
        <div class="q">
          <p>&ldquo;Signed offer in two weeks without my team running a single throwaway screen. The read
            attached to each profile did that work for us.&rdquo;</p>
          <cite>Co-founder, applied ML</cite>
        </div>
      </div>
    </div>
  </section>

{CLOSER}"""

engineers_body = f"""  <section class="sec first">
    <div class="wrap">
      <div class="head">
        <p class="lbl dim">For Engineers</p>
        <div>
          <h1 class="t2">Two Links And You Are In The Pool.</h1>
          <p class="lede">No forms to fill twice, no cover letter. We read your work, then contact you
            only when a role fits.</p>
        </div>
      </div>

      <div class="form rv" data-compose="Engineer intake">
        <div class="fld">
          <label for="e-name">Name</label>
          <input id="e-name" data-label="Name" type="text" placeholder="Your name">
        </div>
        <div class="fld">
          <label for="e-email">Email</label>
          <input id="e-email" data-label="Email" type="email" placeholder="you@domain.com">
        </div>
        <div class="fld">
          <label for="e-li">LinkedIn</label>
          <input id="e-li" data-label="LinkedIn" type="url" placeholder="linkedin.com/in/">
        </div>
        <div class="fld">
          <label for="e-gh">GitHub</label>
          <input id="e-gh" data-label="GitHub" type="url" placeholder="github.com/">
        </div>
        <div class="fld">
          <label for="e-work">Best piece of work</label>
          <input id="e-work" data-label="Best work" type="url" placeholder="A repo, a PR, or something you shipped">
        </div>
        <div class="fld">
          <label for="e-years">Years writing code professionally</label>
          <select id="e-years" data-label="Experience">
            <option value="">Select</option>
            <option>0 to 2 years</option>
            <option>2 to 4 years</option>
            <option>4 to 6 years</option>
            <option>6 to 8 years</option>
            <option>8 years or more</option>
          </select>
        </div>
        <div class="fld">
          <label for="e-when">Timeline</label>
          <select id="e-when" data-label="Timeline">
            <option value="">Select</option>
            <option>Looking now</option>
            <option>Open in the next three months</option>
            <option>Open in six months</option>
            <option>Only for the right role</option>
          </select>
        </div>
        <div class="fld">
          <label for="e-where">Location and remote preference</label>
          <input id="e-where" data-label="Location" type="text" placeholder="City, and onsite / hybrid / remote">
        </div>
        <div class="fld">
          <label for="e-auth">Work authorization</label>
          <input id="e-auth" data-label="Work authorization" type="text" placeholder="Citizen, green card, visa type">
        </div>
        <div class="fld">
          <label for="e-comp">Comp band you would move for</label>
          <input id="e-comp" data-label="Comp expectation" type="text" placeholder="Base, and how you weigh equity">
        </div>
        <div class="fld wide">
          <label for="e-want">What you want next</label>
          <textarea id="e-want" data-label="What they want next"
            placeholder="One or two lines. Stage, scope, the kind of problem."></textarea>
        </div>
      </div>
      <div class="formfoot rv">
        <button class="btn" type="button" data-send>Join the pool</button>
        <p>This opens an email with your answers filled in, so you can see what we get before you send
          it. Nothing costs you anything, ever.</p>
      </div>
    </div>
  </section>

  <section class="sec">
    <div class="wrap">
      <div class="grid rv">
        <div class="cell">
          <span class="n">What you get</span>
          <ul>
            <li>Written feedback on your code from a senior engineer, offer or no offer.</li>
            <li>Salary bands and what the equity is worth before the first call.</li>
            <li>A straight answer on runway and how the founders behave under pressure.</li>
            <li>An email at most twice a year. We do not run mass sends.</li>
          </ul>
        </div>
        <div class="cell">
          <span class="n">What we look for</span>
          <ul>
            <li>Work we can open: a repository, a pull request, something you shipped.</li>
            <li>Depth in one area rather than a tour of nine frameworks.</li>
            <li>How quickly you close a gap once someone points it out.</li>
            <li>A real reason you want to move.</li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <section class="band">
    <div class="wrap">
      <h2 class="rv">Your Work Is Easier To Read Than Your R&eacute;sum&eacute;.</h2>
    </div>
  </section>
"""

companies_body = f"""  <section class="sec first">
    <div class="wrap">
      <div class="head">
        <p class="lbl dim">For Companies</p>
        <div>
          <h1 class="t2">Post A Role. We Come Back Within A Day.</h1>
          <p class="lede">Paste the job description you already have. Everything else is optional.</p>
        </div>
      </div>

      <div class="form rv" data-compose="New search">
        <div class="fld">
          <label for="c-company">Company</label>
          <input id="c-company" data-label="Company" type="text" placeholder="Name">
        </div>
        <div class="fld">
          <label for="c-site">Website</label>
          <input id="c-site" data-label="Website" type="url" placeholder="yourcompany.com">
        </div>
        <div class="fld">
          <label for="c-name">Your name and role</label>
          <input id="c-name" data-label="Contact" type="text" placeholder="Who we will be working with">
        </div>
        <div class="fld">
          <label for="c-email">Email</label>
          <input id="c-email" data-label="Email" type="email" placeholder="you@yourcompany.com">
        </div>
        <div class="fld">
          <label for="c-stage">Stage</label>
          <select id="c-stage" data-label="Stage">
            <option value="">Select</option>
            <option>Pre-seed</option>
            <option>Seed</option>
            <option>Series A</option>
            <option>Series B</option>
            <option>Series C</option>
            <option>Growth</option>
          </select>
        </div>
        <div class="fld">
          <label for="c-size">Engineering team size</label>
          <input id="c-size" data-label="Team size" type="text" placeholder="How many engineers today">
        </div>
        <div class="fld">
          <label for="c-role">Role and level</label>
          <input id="c-role" data-label="Role" type="text" placeholder="Founding engineer, senior backend, infra lead">
        </div>
        <div class="fld">
          <label for="c-stack">Stack</label>
          <input id="c-stack" data-label="Stack" type="text" placeholder="Languages, infrastructure, anything non-obvious">
        </div>
        <div class="fld">
          <label for="c-reviewer">Who reviews the code</label>
          <input id="c-reviewer" data-label="Code reviewer" type="text" placeholder="The engineer who approves the first pull request">
        </div>
        <div class="fld">
          <label for="c-start">When you need someone</label>
          <input id="c-start" data-label="Start date" type="text" placeholder="A date or a quarter">
        </div>
        <div class="fld wide">
          <label for="c-link">Link to the job posting</label>
          <input id="c-link" data-label="Job posting link" type="url" placeholder="Your careers page, Ashby, Greenhouse, a Notion doc">
        </div>
        <div class="fld wide">
          <label for="c-jd">Or paste the job description</label>
          <textarea id="c-jd" data-label="Job description"
            placeholder="Paste it here. Rough notes are fine, we do not need it polished."></textarea>
        </div>
      </div>
      <div class="formfoot rv">
        <button class="btn" type="button" data-send>Send the role</button>
        <p>This opens an email with everything filled in, so you can read it before it goes. No fee is
          owed unless we place someone.</p>
      </div>
    </div>
  </section>

  <section class="sec" id="roles">
    <div class="wrap">
      <div class="head rv">
        <p class="lbl dim">What We Search For</p>
        <div><h2>Early And Mid-Level Engineering Roles.</h2></div>
      </div>
      <table class="tbl rv">
        <thead>
          <tr><th>Role</th><th>Experience</th><th>What we screen for</th></tr>
        </thead>
        <tbody>
          <tr><td class="k">Founding engineer</td><td class="w">0&ndash;4 yrs</td>
            <td>Has built something end to end without anyone checking on them.</td></tr>
          <tr><td class="k">Backend and distributed systems</td><td class="w">2&ndash;7 yrs</td>
            <td>Can tell you what breaks first in a system and why.</td></tr>
          <tr><td class="k">Infrastructure and platform</td><td class="w">3&ndash;8 yrs</td>
            <td>Has owned a build or deploy path that other teams relied on.</td></tr>
          <tr><td class="k">Applied ML and inference</td><td class="w">2&ndash;7 yrs</td>
            <td>Measures the work. Benchmarks and latency budgets, not demos.</td></tr>
          <tr><td class="k">Forward-deployed engineer</td><td class="w">2&ndash;6 yrs</td>
            <td>Writes code in front of a customer and stays comfortable doing it.</td></tr>
          <tr><td class="k">Full-stack product engineer</td><td class="w">1&ndash;6 yrs</td>
            <td>Ships user-facing work quickly without leaving a mess behind.</td></tr>
        </tbody>
      </table>
    </div>
  </section>

  <section class="sec">
    <div class="wrap">
      <div class="grid rv">
        <div class="cell">
          <span class="n">What happens next</span>
          <ul>
            <li>We reply the same day with a time to talk, or the date we can start.</li>
            <li>A sixty-minute call with whoever reviews the code.</li>
            <li>A written scorecard you approve before we contact anyone.</li>
            <li>First introductions inside two weeks.</li>
            <li>No fee is owed unless we place someone.</li>
          </ul>
        </div>
        <div class="cell">
          <span class="n">Who we work with</span>
          <ul>
            <li>US-based engineering teams, seed through growth stage.</li>
            <li>Early and mid-level hires, from founding engineer to infrastructure lead.</li>
            <li>We do not run senior or executive searches.</li>
          </ul>
        </div>
      </div>
    </div>
  </section>
"""

pages = {
    "index.html": ("Foray | Your autonomous recruiting agent",
                   "Message Foray and we find roles worth your time, write the application, and apply for you. A human reviews everything, and nothing sends without your yes.",
                   index_body),
    "engineers.html": ("For engineers | Foray",
                       "Join the Foray pool with your LinkedIn and GitHub. We contact you only when a role fits.",
                       engineers_body),
    "companies.html": ("For companies | Foray",
                       "Post an engineering role to Foray. Paste your job description and we reply within a day.",
                       companies_body),
}

for name, (title, desc, body) in pages.items():
    html = landing(title, desc) if name == "index.html" else shell(name, title, desc, body)
    (OUT / name).write_text(html, encoding="utf-8")
    print("wrote", name, f"{len((OUT / name).read_text(encoding='utf-8')) // 1024} KB")
