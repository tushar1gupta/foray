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
  var FRAMES=["\n         xx=\n        +xx*\n        x++o:\n        +x**\n         x*=\n         +o\n      .+xx**o.\n      ==xx**++\n      =;xx**=+\n      =;x***=+\n      =;x***=+\n      =;x***=+\n      =;x**#=o\n      =;x***=o\n      =;o**x=+\n      =;+x*+=+\n         xx\n         xx\n         xx\n         xx\n         xx\n         ox\n         ox\n         ox\n         =+\n", "\n         :+\n        :xx*\n        xxx*.\n        xxo*.\n         x**\n         +o\n       +xx**o\n     ;==xx**+++\n     ;=;xx**=++\n     ==:x***:++\n     ==.x***:+o\n     ==.x***.+o\n     == x**# oo\n     == x*** oo\n     == x*** +o\n     ==:x***.+o\n     ..:x=:*.::\n       :o=:x.\n       :o=:x.\n       :o=:x.\n       :o=:x.\n       :o=:x.\n       :o=:x.\n       +o==oo\n       ;+.\n", "\n         =x.\n        =xx*\n        xo+*:\n        ox**\n         x*x\n         +o\n       +xx**o\n    .; =xx**+.+.\n    .; ;xx**=.+.\n    .= :x***:.+.\n    .= .x***..o.\n    .= .x***..o.\n    .=  x**# .o:\n    .=  x*** .o:\n    .= .x***:.o.\n    .=.oo**o*.o.\n     ..oo  ;* .\n      .oo  ;*\n      .oo  ;*\n      .oo  ;*\n      .o+  ;x\n      .o+  ;x\n      .o+  ;xx.\n      +o+   ..\n      ==.\n", "\n         xxx\n        oxx*\n        x++o:\n        =x**\n         +x.\n         +o\n    .: +xx**o :.\n    .; =xx**+.+.\n    .; :xx**;.+.\n    .= :x***:.+.\n    .= .x***..o.\n    .=  x*** .o.\n    .=  x**# .o:\n    .=  x*** .o:\n    .=.+o**xo.o.\n    .;.oo  ;*.+.\n      .oo  ;*\n      .oo  ;*\n      .oo  ;*\n      .oo  ;*\n      .o+  ;x\n      .o+  ;x\n      .o+  ;xx.\n      +o+   ..\n      ==.\n", "\n         xxx\n        oxx*.\n        x++o.\n        :x**\n         =o\n         +o\n     ::=xx**o;;\n     ;=;xx**+++\n     ;=:xx**;++\n     ==:x***:++\n     ==.x***.+o\n     == x*** +o\n     == x**# oo\n     == x*** oo\n     ==:o**x.+o\n     ;;:x=:*.++\n       :x=:*.\n       :o=:x.\n       :o=:x.\n       :o=:x.\n       :o=:x.\n       :o=:x.\n       :o=:x.\n       +o==oo\n       ;+.\n", "\n         xx=\n        +xx*\n        x++o:\n        +x**\n         x*=\n         +o\n      .+xx**o.\n      ==xx**++\n      =;xx**=+\n      =;x***=+\n      =;x***=+\n      =;x***=+\n      =;x**#=o\n      =;x***=o\n      =;o**x=+\n      =;+x*+=+\n         xx\n         xx\n         xx\n         xx\n         xx\n         ox\n         ox\n         ox\n         =+\n", "\n         :+\n        :xx*\n        xxx*.\n        xxo*.\n         x**\n         +o\n       +xx**o\n      .=xx**+.\n      .=xx**+.\n      .=x***+.\n      .=x***+.\n      .=x***+.\n      .=x**#+.\n      .=x***+.\n      .=x***+.\n      .=x***+.\n      .:x=:*:.\n       :o=:x.\n       :o=:x.\n       :o=:x.\n       :o=:x.\n       :o=:x.\n       :o=:x.\n       +o==oo\n       ;+.\n", "\n         =x.\n        =xx*\n        xo+*:\n        ox**\n         x*x\n         +o\n       +xx**o\n       =xx**+\n       =xx**+\n       =x***+\n       =x***+\n       =x***+\n       =x**#+\n       =x***+\n       =x***+\n      .oo**o*\n      .oo  ;*\n      .oo  ;*\n      .oo  ;*\n      .oo  ;*\n      .o+  ;x\n      .o+  ;x\n      .o+  ;xx.\n      +o+   ..\n      ==.\n", "\n         xxx\n        oxx*\n        x++o:\n        =x**\n         +x.\n         +o\n       +xx**o\n       =xx**+\n       =xx**+\n       =x***+\n       =x***+\n       =x***+\n       =x**#+\n       =x***+\n      .+o**xo\n      .oo  +*\n      .oo  ;*\n      .oo  ;*\n      .oo  ;*\n      .oo  ;*\n      .o+  ;x\n      .o+  ;x\n      .o+  ;xx.\n      +o+   ..\n      ==.\n", "\n         xxx\n        oxx*.\n        x++o.\n        :x**\n         =o\n         +o\n      .=xx**o.\n      .=xx**+.\n      .=xx**+.\n      .=x***+.\n      .=x***+.\n      .=x***+.\n      .=x**#+.\n      .=x***+.\n      .=o**x+.\n      .;x=:*=.\n       :x=:*.\n       :o=:x.\n       :o=:x.\n       :o=:x.\n       :o=:x.\n       :o=:x.\n       :o=:x.\n       +o==oo\n       ;+.\n"];
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
        window.location.href='mailto:contact@goforay.io?subject='+
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