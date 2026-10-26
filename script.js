/* OmKiran Bhakti — small, dependency-free site script */
(function(){
  var store={get:function(k){try{return localStorage.getItem(k)}catch(e){return null}},
             set:function(k,v){try{localStorage.setItem(k,v)}catch(e){}}};

  // Theme
  var root=document.documentElement, saved=store.get('okb-theme');
  if(saved) root.setAttribute('data-theme',saved);
  var tb=document.querySelector('.theme-btn');
  if(tb) tb.addEventListener('click',function(){
    var dark=root.getAttribute('data-theme')==='dark'||(!root.getAttribute('data-theme')&&matchMedia('(prefers-color-scheme: dark)').matches);
    var next=dark?'light':'dark'; root.setAttribute('data-theme',next); store.set('okb-theme',next);
  });

  // Language: Hindi by default. English only if the visitor chooses it (remembered),
  // or — as a one-tap suggestion, never a forced switch — when the browser is a non-Indian English one.
  (function(){
    var sw=document.querySelector('.lang-sw'); if(!sw) return;
    var hiA=sw.querySelector('[lang="hi"]'), enA=sw.querySelector('[data-lang="en"]');
    var onProxy=/\.translate\.goog$/.test(location.hostname);
    var path=location.pathname.replace(/^\/en\//,'/');
    var hiURL='https://omkiranbhakti.com'+path+'?lang=hi';
    if(onProxy){  // Google-translated view: lyrics and holy names stay untranslated, shown in Roman letters
      document.querySelectorAll('[data-ro]').forEach(function(el){ el.textContent=el.getAttribute('data-ro'); });
      var ro=document.querySelector('.section.ro-sec'); if(ro) ro.style.display='none';
    }
    if(onProxy||/^\/en\//.test(location.pathname)){           // we are on an English view
      hiA.classList.remove('on'); hiA.removeAttribute('aria-current'); hiA.href=hiURL;
      enA.classList.add('on'); enA.setAttribute('aria-current','true'); enA.removeAttribute('href');
      return;
    }
    var q=new URLSearchParams(location.search);
    if(q.get('lang')==='hi'){ store.set('okb-lang','hi'); history.replaceState(null,'',location.pathname+location.hash); }
    enA.addEventListener('click',function(){ store.set('okb-lang','en'); });
    hiA.addEventListener('click',function(e){ e.preventDefault(); store.set('okb-lang','hi'); });
    var pref=store.get('okb-lang');
    if(pref==='en'){ location.replace(enA.href); return; }
    if(pref) return;
    var bot=/bot|crawl|spider|slurp|lighthouse|headless/i.test(navigator.userAgent)||navigator.webdriver;
    var langs=(navigator.languages&&navigator.languages.length?navigator.languages:[navigator.language||'']).map(function(l){return (l||'').toLowerCase()});
    var tz=''; try{tz=Intl.DateTimeFormat().resolvedOptions().timeZone||''}catch(e){}
    var indian=/Calcutta|Kolkata/.test(tz)||langs.some(function(l){return l.indexOf('hi')===0||/-in$/.test(l)});
    if(bot||indian||langs[0].indexOf('en')!==0) return;
    var b=document.createElement('div'); b.className='lang-tip no-print'; b.setAttribute('role','dialog'); b.setAttribute('aria-label','Language');
    b.innerHTML='<span lang="en">Prefer to read this page in English?</span><a class="btn" lang="en" href="'+enA.href+'">Read in English</a><button type="button" class="btn ghost">हिंदी में ही पढ़ें</button>';
    b.querySelector('a').addEventListener('click',function(){ store.set('okb-lang','en'); });
    b.querySelector('button').addEventListener('click',function(){ store.set('okb-lang','hi'); b.remove(); });
    document.body.appendChild(b);
  })();

  // English pages: show/hide the Devanagari line
  document.querySelectorAll('[data-dev]').forEach(function(b){b.addEventListener('click',function(){
    var on=document.body.classList.toggle('no-dev'); b.setAttribute('aria-pressed',!on);});});

  // Mobile menu
  var mb=document.querySelector('.menu-btn'), nav=document.querySelector('.nav');
  if(mb&&nav) mb.addEventListener('click',function(){var o=nav.classList.toggle('open');mb.setAttribute('aria-expanded',o)});

  // Lite YouTube: load the player only when asked
  document.addEventListener('click',function(e){
    var b=e.target.closest&&e.target.closest('.play'); if(!b) return;
    var id=b.getAttribute('data-id'), f=document.createElement('iframe');
    f.src='https://www.youtube-nocookie.com/embed/'+id+'?autoplay=1&rel=0';
    f.title=b.getAttribute('aria-label')||'वीडियो';
    f.allow='accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture'; f.allowFullscreen=true;
    b.parentNode.appendChild(f); b.remove();
  });

  // Lyrics reader controls
  var ly=document.querySelector('.lyrics');
  if(ly){
    var size=parseFloat(store.get('okb-ls'))||1.45;
    var apply=function(){ly.style.setProperty('--ls',size+'rem')}; apply();
    document.querySelectorAll('[data-size]').forEach(function(b){b.addEventListener('click',function(){
      size=Math.min(2.4,Math.max(1.1,size+parseFloat(b.dataset.size)));apply();store.set('okb-ls',size)})});
    var mt=document.querySelector('[data-meaning]');
    if(mt) mt.addEventListener('click',function(){var on=mt.getAttribute('aria-pressed')==='true';
      mt.setAttribute('aria-pressed',!on);ly.classList.toggle('no-meaning',on)});
    var pr=document.querySelector('[data-print]'); if(pr) pr.addEventListener('click',function(){window.print()});
  }

  // "Aaj" card on the home page: festival first, otherwise the weekday's traditional deity
  var today=document.getElementById('today');
  if(today){
    var d=new Date(), ist=new Date(d.getTime()+(d.getTimezoneOffset()+330)*60000);
    var ymd=ist.getFullYear()*10000+(ist.getMonth()+1)*100+ist.getDate();
    var navratri={20261011:'पहला दिन — माँ शैलपुत्री',20261012:'दूसरा दिन — माँ ब्रह्मचारिणी',20261013:'तीसरा दिन — माँ चंद्रघंटा',
      20261014:'चौथा दिन — माँ कूष्मांडा',20261015:'पाँचवाँ दिन — माँ स्कंदमाता',20261016:'छठा दिन — माँ कात्यायनी',
      20261017:'सातवाँ दिन — माँ कालरात्रि',20261018:'नवरात्रि — अष्टमी की तैयारी',20261019:'अष्टमी व नवमी — माँ महागौरी व माँ सिद्धिदात्री',20261020:'विजयादशमी (दशहरा)'};
    var week=[
      ['रविवार','सूर्य देव और श्रीराम','रविवार सूर्य देव की उपासना का दिन है। सूर्यवंशी श्रीराम की स्तुति और राम चालीसा भी सुनें।','ram-bhajan.html','राम भजन सुनें'],
      ['सोमवार','भगवान शिव','सोमवार भोलेनाथ का दिन है। शिव आरती और शिव चालीसा का पाठ करें।','shiv-aarti-om-jai-shiv-omkara.html','शिव आरती पढ़ें'],
      ['मंगलवार','हनुमान जी','मंगलवार बजरंगबली का दिन है। हनुमान चालीसा का पाठ करें।','hanuman-chalisa.html','हनुमान चालीसा पढ़ें'],
      ['बुधवार','श्री गणेश','बुधवार विघ्नहर्ता गणेश जी का दिन है। गणेश आरती गाएँ।','ganesh-aarti-jai-ganesh-deva.html','गणेश आरती पढ़ें'],
      ['गुरुवार','भगवान विष्णु','गुरुवार श्रीहरि विष्णु का दिन है। ॐ जय जगदीश हरे आरती गाएँ।','om-jai-jagdish-hare-aarti.html','जगदीश आरती पढ़ें'],
      ['शुक्रवार','माता रानी','शुक्रवार देवी माँ का दिन है। माता रानी के भजन सुनें।','mata-rani-bhajan.html','माता रानी भजन'],
      ['शनिवार','शनि देव और हनुमान जी','शनिवार को शनि देव और हनुमान जी का स्मरण किया जाता है।','hanuman-chalisa.html','हनुमान चालीसा पढ़ें']];
    var navArt={20261011:'Ht_SogxJ_D8',20261012:'SsrEdkAf4xI',20261013:'lUhDATRpvrs',20261014:'65nhAnBmYuQ',20261015:'Q5_3JBKLNpg',
      20261016:'r32U54qyerw',20261017:'FFcNanFHSaY',20261018:'@mahagauri',20261019:'@siddhidatri',20261020:'pCixItfj5Vo'};
    var weekArt=[['pCixItfj5Vo',80,'जय श्री राम'],['Kbe3pbLsg1U',80,'हर हर महादेव'],['707iS1Iyv-E',12,'जय बजरंगबली'],['NGI-JiRiwSc',80,'गणपति बप्पा मोरया'],
      ['pCixItfj5Vo',80,'ॐ नमो नारायणाय'],['2yVR5zSaKpc',76,'जय माता दी'],['707iS1Iyv-E',12,'जय बजरंगबली']];
    var art=document.querySelector('#today-art img'), cap=document.getElementById('today-cap');
    var LOC={'2yVR5zSaKpc':'mata','Kbe3pbLsg1U':'shiv','707iS1Iyv-E':'hanuman','NGI-JiRiwSc':'ganesh','pCixItfj5Vo':'ram','G99-49Pfs6U':'navdurga','Ht_SogxJ_D8':'shailputri','SsrEdkAf4xI':'brahmacharini','lUhDATRpvrs':'chandraghanta','65nhAnBmYuQ':'kushmanda','Q5_3JBKLNpg':'skandamata','r32U54qyerw':'katyayani','FFcNanFHSaY':'kalaratri'};
    function setArt(id,pos,c){if(!art)return;if(id.charAt(0)==='@'){art.src='img/art/'+id.slice(1)+'.webp';art.style.objectPosition='50% 22%';if(cap)cap.textContent=c;return;}if(LOC[id]){art.onerror=null;art.src='img/art/'+LOC[id]+'.webp';art.style.objectPosition='50% 22%';if(cap)cap.textContent=c;return;}art.onerror=function(){art.onerror=null;art.src='https://i.ytimg.com/vi/'+id+'/hqdefault.jpg'};
      art.src='https://i.ytimg.com/vi/'+id+'/maxresdefault.jpg';art.style.objectPosition=pos+'% 30%';if(cap)cap.textContent=c;}
    if(navArt[ymd]) setArt(navArt[ymd], navArt[ymd]==='G99-49Pfs6U'?50:(navArt[ymd]==='pCixItfj5Vo'?80:68), ymd===20261020?'जय श्री राम':'जय माता दी');
    else { var wa=weekArt[ist.getDay()]; setArt(wa[0],wa[1],wa[2]); }
    var w=week[ist.getDay()], h=today.querySelector('h2'), p=today.querySelector('p.say'), a=today.querySelector('a.go'), when=today.querySelector('.when');
    if(navratri[ymd]){when.textContent='आज · शारदीय नवरात्रि 2026';h.textContent=navratri[ymd];
      p.textContent='नवरात्रि के हर दिन देवी के एक स्वरूप की पूजा होती है। आज की आरती और पूरे नौ दिनों की सूची देखें।';a.href='navratri-2026.html';a.textContent='नवरात्रि 2026 पेज खोलें';}
    else{when.textContent='आज '+w[0];h.textContent=w[1];p.textContent=w[2];a.href=w[3];a.textContent=w[4];}
  }

  // Navratri page: highlight today
  document.querySelectorAll('.days li[data-ymd]').forEach(function(li){
    var d=new Date(), ist=new Date(d.getTime()+(d.getTimezoneOffset()+330)*60000);
    var ymd=String(ist.getFullYear()*10000+(ist.getMonth()+1)*100+ist.getDate());
    if(li.dataset.ymd.split(',').indexOf(ymd)>-1){li.classList.add('now');var dv=li.querySelector('div:not(.arch)')||li;dv.insertAdjacentHTML('afterbegin','<strong style="color:var(--sindoor)">आज · </strong>');}
  });

  // Jaap mala
  var mala=document.getElementById('mala');
  if(mala){
    var svg=mala.querySelector('svg'), N=108, beads=[];
    for(var i=0;i<N;i++){var t=(i/N)*Math.PI*2-Math.PI/2, c=document.createElementNS('http://www.w3.org/2000/svg','circle');
      c.setAttribute('cx',(200+182*Math.cos(t)).toFixed(2));c.setAttribute('cy',(200+182*Math.sin(t)).toFixed(2));c.setAttribute('r',6.2);
      c.setAttribute('class','bead');svg.appendChild(c);beads.push(c);}
    var s=document.createElementNS('http://www.w3.org/2000/svg','circle');s.setAttribute('cx',200);s.setAttribute('cy',8);s.setAttribute('r',10);s.setAttribute('class','bead sumeru');svg.appendChild(s);
    var count=parseInt(store.get('okb-count'))||0, malas=parseInt(store.get('okb-malas'))||0, total=parseInt(store.get('okb-total'))||0;
    var sel=document.getElementById('mantra'), custom=document.getElementById('custom'), show=mala.querySelector('.mantra-show');
    var cEl=mala.querySelector('.count'), mEl=document.getElementById('malas'), tEl=document.getElementById('total');
    var savedM=store.get('okb-mantra'); if(savedM){ if([].some.call(sel.options,function(o){return o.value===savedM})) sel.value=savedM; else {sel.value='custom';custom.value=savedM;} }
    function mantra(){return sel.value==='custom'?(custom.value.trim()||'अपना मंत्र लिखें'):sel.value}
    function draw(){cEl.textContent=count;mEl.textContent=malas;tEl.textContent=total;show.textContent=mantra();
      custom.parentNode.hidden=sel.value!=='custom';beads.forEach(function(b,i){b.classList.toggle('on',i<count)});}
    function save(){store.set('okb-count',count);store.set('okb-malas',malas);store.set('okb-total',total);store.set('okb-mantra',mantra())}
    function tap(){count++;total++;if(count>=N){count=0;malas++;if(navigator.vibrate)navigator.vibrate([80,60,80]);}
      else if(navigator.vibrate)navigator.vibrate(12);draw();save();}
    mala.querySelector('.tap').addEventListener('click',tap);
    document.addEventListener('keydown',function(e){if((e.code==='Space'||e.key==='Enter')&&e.target===document.body){e.preventDefault();tap();}});
    sel.addEventListener('change',function(){draw();save()}); custom.addEventListener('input',function(){draw();save()});
    document.getElementById('reset').addEventListener('click',function(){count=0;draw();save()});
    draw();
  }

  // ---------- Panchang card: always show today's data (IST) ----------
  var pc=document.getElementById('pcard');
  function istDate(){var d=new Date(),t=new Date(d.getTime()+(d.getTimezoneOffset()+330)*60000);
    var m=('0'+(t.getMonth()+1)).slice(-2),dd=('0'+t.getDate()).slice(-2);return t.getFullYear()+'-'+m+'-'+dd;}
  var MON=['','जनवरी','फ़रवरी','मार्च','अप्रैल','मई','जून','जुलाई','अगस्त','सितंबर','अक्टूबर','नवंबर','दिसंबर'];
  function t12(s){var a=s.split(':'),h=+a[0],m=a[1];var part=h<4?'रात':h<12?'सुबह':h<16?'दोपहर':h<19?'शाम':'रात';return part+' '+(h%12||12)+':'+m;}
  function endTxt(p){if(!p.tithi_end)return '';var day=p.tithi_end.slice(0,10),tm=p.tithi_end.slice(11);return (day===p.date?'आज ':'कल ')+t12(tm)+' तक, फिर '+p.next_tithi;}
  function fill(p){
    var q=function(k){return pc.querySelector('[data-k="'+k+'"]')||document.createElement('span')}, dd=p.date.split('-');
    q('gdate').textContent=(+dd[2])+' '+MON[+dd[1]]+' '+dd[0]+', '+p.vaar;
    q('tithi').textContent=p.paksha+' पक्ष '+p.tithi; q('month').textContent=p.month_purnimanta+' मास'+(p.adhik?' (अधिक मास)':'');
    q('vs').textContent=p.vs; q('tend').textContent=endTxt(p); q('nak').textContent=p.nakshatra;
    q('sunrise').textContent=t12(p.sunrise); q('sunset').textContent=t12(p.sunset);
    q('brahma').textContent=t12(p.brahma[0])+' – '+t12(p.brahma[1]);
    q('abhijit').textContent=t12(p.abhijit[0])+' – '+t12(p.abhijit[1])+(p.abhijit_ok?'':' (बुधवार को नहीं माना जाता)');
    q('rahu').textContent=t12(p.rahu[0])+' – '+t12(p.rahu[1]); q('pradosh').textContent=t12(p.pradosh[0])+' – '+t12(p.pradosh[1]);
    var ul=q('fest'); ul.innerHTML='';
    if(!p.fest.length){ul.innerHTML='<li class="muted">आज कोई बड़ा त्योहार नहीं है</li>';}
    p.fest.forEach(function(f){var li=document.createElement('li'),a=document.createElement('a');a.href=f[2];a.textContent=f[0];
      var sp=document.createElement('span');sp.textContent=' '+f[1];li.appendChild(a);li.appendChild(sp);ul.appendChild(li);});
    pc.setAttribute('data-date',p.date); pc._p=p;
  }
  if(pc){
    var today=istDate();
    if(pc.getAttribute('data-date')!==today){
      fetch('panchang/'+today.slice(0,7)+'.json').then(function(r){return r.ok?r.json():null}).then(function(j){if(j&&j[today])fill(j[today]);}).catch(function(){});
    }
    var sb=pc.querySelector('[data-share]');
    if(sb) sb.addEventListener('click',function(){
      var g=function(k){var el=pc.querySelector('[data-k="'+k+'"]');return el?el.textContent:''};
      var fest=[].map.call(pc.querySelectorAll('[data-k="fest"] a'),function(a){return a.textContent}).join(', ');
      var txt='🙏 आज का पंचांग — '+g('gdate')+'\n🌙 तिथि: '+g('tithi')+' ('+g('month')+')\n⭐ नक्षत्र: '+g('nak')+
        '\n🌅 सूर्योदय '+g('sunrise')+' | सूर्यास्त '+g('sunset')+'\n✨ अभिजीत मुहूर्त: '+g('abhijit')+'\n⚠️ राहु काल: '+g('rahu')+
        (fest?'\n🪔 आज: '+fest:'')+'\n\nपूरा पंचांग: https://omkiranbhakti.github.io/aaj-ka-panchang.html';
      window.open('https://wa.me/?text='+encodeURIComponent(txt),'_blank','noopener');
    });
  }

  // ---------- Library search ----------
  var lq=document.getElementById('lib-q');
  if(lq){
    var items=[].slice.call(document.querySelectorAll('.paath li')), cnt=document.getElementById('lib-count');
    var secs=[].slice.call(document.querySelectorAll('section[id]')).filter(function(s){return s.querySelector('.paath')});
    var alias={'hanuman':'हनुमान','shiv':'शिव','shiva':'शिव','durga':'दुर्गा','ganesh':'गणेश','krishna':'कृष्ण','ram':'राम','lakshmi':'लक्ष्मी','laxmi':'लक्ष्मी','shani':'शनि','saraswati':'सरस्वती','surya':'सूर्य','aarti':'आरती','chalisa':'चालीसा','mantra':'मंत्र','katha':'कथा','vishnu':'विष्णु','gayatri':'गायत्री','ganga':'गंगा','tulsi':'तुलसी'};
    var dvs=[].slice.call(document.querySelectorAll('.dv')), dsel='';
    var DN={devi:'देवी माँ',shiv:'शिव',hanuman:'हनुमान',ganesh:'गणेश',krishna:'कृष्ण',vishnu:'राम और विष्णु',lakshmi:'लक्ष्मी',shani:'शनि',surya:'सूर्य'};
    function run(){
      var q=lq.value.trim().toLowerCase(); var qq=alias[q]||q; var n=0;
      items.forEach(function(li){var t=li.textContent.toLowerCase()+' '+(li.querySelector('a').getAttribute('href')||'');
        var ok=(!q||t.indexOf(qq)>-1||t.indexOf(q)>-1)&&(!dsel||li.getAttribute('data-deity')===dsel);li.hidden=!ok;if(ok)n++;});
      secs.forEach(function(s){s.hidden=!s.querySelector('.paath li:not([hidden])');});
      cnt.textContent=(q||dsel)?(n+' पाठ मिले'+(dsel?' — '+DN[dsel]:'')):'';
    }
    function pick(k){ dsel=(dsel===k)?'':k; dvs.forEach(function(b){b.setAttribute('aria-pressed',b.getAttribute('data-dv')===dsel?'true':'false')}); run();
      if(dsel){var f=document.querySelector('.paath li:not([hidden])'); if(f){var sec=f.closest('section'); if(sec) sec.scrollIntoView({behavior:'smooth',block:'start'});}} }
    dvs.forEach(function(b){b.addEventListener('click',function(){pick(b.getAttribute('data-dv'))})});
    var today=document.getElementById('dv-today');
    if(today){
      var W=[['रविवार','surya','सूर्य देव'],['सोमवार','shiv','भगवान शिव'],['मंगलवार','hanuman','हनुमान जी'],['बुधवार','ganesh','गणेश जी'],['गुरुवार','vishnu','भगवान विष्णु'],['शुक्रवार','devi','माँ दुर्गा और लक्ष्मी'],['शनिवार','shani','शनि देव और हनुमान जी']][new Date().getDay()];
      today.innerHTML='आज '+W[0]+' है — '+W[2]+' का दिन। <button type="button" class="linkish" data-today="'+W[1]+'">इनके पाठ देखें</button>';
      today.hidden=false;
      today.querySelector('button').addEventListener('click',function(){pick(W[1])});
    }
    lq.addEventListener('input',run);
  }

  /* ---- paath mode: lamp-lit full page, screen stays awake ---- */
  (function(){
    var btns=document.querySelectorAll('[data-paath]'), sec=document.querySelector('.paath-sec');
    if(!btns.length||!sec) return;
    var root=document.documentElement, lock=null, bar=document.createElement('div');
    bar.className='paath-progress'; bar.setAttribute('aria-hidden','true'); document.body.appendChild(bar);
    function prog(){ if(!root.classList.contains('paath-on')) return;
      var max=document.documentElement.scrollHeight-innerHeight; bar.style.width=(max>0?Math.min(100,scrollY/max*100):0)+'%'; }
    function wake(){ try{ if('wakeLock' in navigator) navigator.wakeLock.request('screen').then(function(l){lock=l}).catch(function(){}); }catch(e){} }
    function set(on){
      root.classList.toggle('paath-on',on);
      btns.forEach(function(b){ if(b.classList.contains('chip')) b.setAttribute('aria-pressed',on?'true':'false'); });
      if(on){ window.scrollTo(0,0); wake(); }
      else { if(lock){ try{lock.release()}catch(e){} lock=null; } sec.scrollIntoView(); }
      prog();
    }
    btns.forEach(function(b){ b.addEventListener('click',function(){ set(!root.classList.contains('paath-on')); }); });
    addEventListener('scroll',prog,{passive:true});
    addEventListener('keydown',function(ev){ if(ev.key==='Escape'&&root.classList.contains('paath-on')) set(false); });
    document.addEventListener('visibilitychange',function(){ if(document.visibilityState==='visible'&&root.classList.contains('paath-on')) wake(); });
  })();
})();

/* OmKiran Bhakti own bhajan player (MP3, no ads). list = [{t:title, f:url}]
   Starts at 20% volume (the viewer's own choice is remembered), with volume slider, mute, prev/next and a track list. */
window.okbAudio=function(box,list){
  if(!box||!list||!list.length)return;
  if(box._a){box._a.pause();}
  var VK='okbVol',vol=0.2;try{var sv=parseFloat(localStorage.getItem(VK));if(sv>=0&&sv<=1)vol=sv;}catch(e){}
  box.classList.add('is-audio');
  var opts='';for(var k=0;k<list.length;k++)opts+='<option value="'+k+'">'+(k+1)+'. '+String(list[k].t).replace(/</g,'&lt;')+'</option>';
  box.innerHTML='<div class="okb-ap"><div class="ap-info"><b class="ap-t"></b><div class="ap-bar" role="slider" aria-label="भजन में आगे-पीछे"><i></i></div><small class="ap-n"></small></div>'+
    '<button type="button" class="ap-b ap-prev" aria-label="पिछला भजन">⏮</button>'+
    '<button type="button" class="ap-b ap-play" aria-label="चलाएँ / रोकें">▶</button><button type="button" class="ap-b ap-next" aria-label="अगला भजन">⏭</button>'+
    '<div class="ap-vol"><button type="button" class="ap-b ap-mute" aria-label="आवाज़ बंद / चालू">🔉</button>'+
    '<input type="range" class="ap-vr" min="0" max="100" step="1" aria-label="आवाज़ (वॉल्यूम)"></div>'+
    (list.length>1?'<label class="ap-list"><span>भजन चुनें</span><select class="ap-sel">'+opts+'</select></label>':'')+
    '<audio preload="none"></audio></div>';
  var a=box.querySelector('audio'),t=box.querySelector('.ap-t'),n=box.querySelector('.ap-n'),bar=box.querySelector('.ap-bar i'),pl=box.querySelector('.ap-play'),
      vr=box.querySelector('.ap-vr'),mu=box.querySelector('.ap-mute'),sel=box.querySelector('.ap-sel'),i=0;
  box._a=a;
  function icon(){mu.textContent=(a.muted||a.volume===0)?'🔇':(a.volume<0.5?'🔉':'🔊');}
  function setVol(v,save){v=Math.max(0,Math.min(1,v));a.volume=v;a.muted=false;vr.value=Math.round(v*100);vr.style.setProperty('--v',vr.value+'%');icon();
    if(save){try{localStorage.setItem(VK,String(v))}catch(e){}}}
  setVol(vol,false);
  function load(k,go){i=(k+list.length)%list.length;a.src=list[i].f;a.volume=parseFloat(vr.value)/100;t.textContent=list[i].t;n.textContent=(i+1)+' / '+list.length+' · OmKiran Bhakti';
    if(sel)sel.value=String(i);
    if(go){var p=a.play();if(p&&p.catch)p.catch(function(){pl.textContent='▶';});}}
  a.addEventListener('play',function(){pl.textContent='⏸';});
  a.addEventListener('pause',function(){pl.textContent='▶';});
  a.addEventListener('ended',function(){load(i+1,true);});
  a.addEventListener('volumechange',icon);
  a.addEventListener('timeupdate',function(){if(a.duration)bar.style.width=(a.currentTime/a.duration*100)+'%';});
  box.querySelector('.ap-bar').addEventListener('click',function(ev){if(a.duration){var r=this.getBoundingClientRect();a.currentTime=(ev.clientX-r.left)/r.width*a.duration;}});
  pl.addEventListener('click',function(){a.paused?a.play():a.pause();});
  box.querySelector('.ap-prev').addEventListener('click',function(){load(i-1,true);});
  box.querySelector('.ap-next').addEventListener('click',function(){load(i+1,true);});
  vr.addEventListener('input',function(){setVol(vr.value/100,true);});
  mu.addEventListener('click',function(){if(a.muted||a.volume===0){setVol(parseFloat(vr.value)>0?vr.value/100:0.2,true);}else{a.muted=true;icon();}});
  if(sel)sel.addEventListener('change',function(){load(parseInt(sel.value,10),true);});
  load(0,true);
};

/* Home welcome: marigold & rose petal shower + greeting (once per visit, skipped for reduced motion) */
(function(){
  if(!document.querySelector('.hero4'))return;
  try{if(window.matchMedia('(prefers-reduced-motion: reduce)').matches)return;}catch(e){}
  try{if(sessionStorage.getItem('okbWelcome'))return;sessionStorage.setItem('okbWelcome','1');}catch(e){}
  var COL=['#ff9f1c','#ffbf3c','#f77f00','#ffd166','#e63946','#ff6f91','#fca311'];
  var box=document.createElement('div');box.className='petal-rain';box.setAttribute('aria-hidden','true');
  var n=window.innerWidth<600?26:44;
  for(var i=0;i<n;i++){var p=document.createElement('i');var c=COL[i%COL.length];
    p.style.left=(Math.random()*100)+'vw';p.style.background='radial-gradient(circle at 30% 30%,#fff6 0,'+c+' 55%)';
    var s=10+Math.random()*12;p.style.width=s+'px';p.style.height=(s*1.35)+'px';
    p.style.animationDuration=(3.2+Math.random()*2.6)+'s,'+(1.4+Math.random()*1.4)+'s';p.style.animationDelay=(Math.random()*1.6)+'s,0s';
    box.appendChild(p);}
  var d=new Date(),g=['ॐ नमः शिवाय','हर हर महादेव','जय बजरंगबली','गणपति बप्पा मोरया','जय श्री हरि','जय माता दी','जय शनिदेव'][d.getDay()];
  var w=document.createElement('div');w.className='welcome-toast';w.setAttribute('role','status');
  w.innerHTML='<span class="wt-om">ॐ</span><span><b>'+g+'</b><small>OmKiran Bhakti में आपका स्वागत है 🙏</small></span>';
  document.body.appendChild(box);document.body.appendChild(w);
  setTimeout(function(){w.classList.add('out')},4200);
  setTimeout(function(){box.remove();w.remove()},7600);
})();

/* Visitor counter (free: abacus.jasoncameron.dev).
   Per page load: pv. Per browser session (first page): visits, day visits, source, device.
   First visit ever from this browser: uniq + day-unique. Footer shows real numbers; hidden if service unreachable. */
(function(){
  var box=document.getElementById('okb-count');if(!box||!window.fetch)return;
  var NS='omkiranbhakti-site',base='https://abacus.jasoncameron.dev/';
  function dkey(off){var d=new Date(Date.now()+(new Date().getTimezoneOffset()+330)*60000-off*864e5);return d.getFullYear()+('0'+(d.getMonth()+1)).slice(-2)+('0'+d.getDate()).slice(-2)}
  var today=dkey(0),ss=null,ls=null;try{ss=sessionStorage;ls=localStorage}catch(e){}
  var newSess=false,newUser=false;
  try{newSess=!ss.getItem('okbC');ss.setItem('okbC','1')}catch(e){}
  try{newUser=!ls.getItem('okbU');if(newUser)ls.setItem('okbU',today)}catch(e){}
  function call(act,k){return fetch(base+act+'/'+NS+'/'+k).then(function(r){return r.ok?r.json():{value:0}}).then(function(j){return j.value>0?j.value:0}).catch(function(){return 0})}
  function src(){
    var q=new URLSearchParams(location.search),u=(q.get('utm_source')||'').toLowerCase(),r='';
    try{r=document.referrer?new URL(document.referrer).hostname:''}catch(e){}
    if(u)r=u; if(r.indexOf('omkiranbhakti')>-1)return '';
    var m=[['google','google'],['bing','bing'],['youtube','youtube'],['youtu.be','youtube'],['whatsapp','whatsapp'],['wa.me','whatsapp'],['facebook','facebook'],['fb.','facebook'],['instagram','instagram'],['t.co','twitter'],['twitter','twitter'],['x.com','twitter'],['chatgpt','ai'],['openai','ai'],['perplexity','ai'],['gemini','ai'],['claude','ai'],['copilot','ai'],['duckduckgo','other-search'],['yahoo','other-search'],['yandex','other-search'],['translate.goog','google']];
    if(!r)return 'direct';
    for(var i=0;i<m.length;i++)if(r.indexOf(m[i][0])>-1)return m[i][1];
    return 'other';
  }
  var jobs=[call('hit','pv')];
  if(newSess){var s=src();jobs.push(call('hit','visits'),call('hit','d'+today));
    if(s)jobs.push(call('hit','src-'+s));
    jobs.push(call('hit','dev-'+(/Mobi|Android|iPhone/i.test(navigator.userAgent)?'mobile':'desktop')));
    var tz='';try{tz=Intl.DateTimeFormat().resolvedOptions().timeZone||''}catch(e){}
    jobs.push(call('hit','geo-'+(/Kolkata|Calcutta/.test(tz)?'india':'abroad')));
  }else{jobs.push(call('get','visits'),call('get','d'+today))}
  jobs.push(newUser?call('hit','uniq'):call('get','uniq'));
  if(newUser)call('hit','u'+today);
  var week=[];for(var i=6;i>=1;i--)week.push(call('get','d'+dkey(i)));
  Promise.all(jobs).then(function(v){
    var pv=v[0],visits=newSess?v[1]:v[1],day=v[2],uniq=v[v.length-1];
    if(!visits)return;
    Promise.all(week).then(function(w){
      w.push(day);var mx=Math.max.apply(null,w)||1;
      var f=function(n){return n.toLocaleString('en-IN')};
      var bars=w.map(function(n,i){return '<i style="height:'+Math.max(8,Math.round(n/mx*100))+'%" title="'+f(n)+'"'+(i==6?' class="t"':'')+'></i>'}).join('');
      box.innerHTML='<span class="oc-live"><span class="dot"></span>भक्त-गणना</span>'+
        '<span class="oc-t"><b>'+f(visits)+'</b><small>कुल दर्शन</small></span>'+
        (uniq?'<span class="oc-t"><b>'+f(uniq)+'</b><small>यूनिक भक्त*</small></span>':'')+
        '<span class="oc-t"><b>'+f(day)+'</b><small>आज</small></span>'+
        '<span class="oc-w" aria-label="पिछले 7 दिन">'+bars+'<small>पिछले 7 दिन</small></span>'+
        (uniq?'<span class="oc-note">*यूनिक गिनती 18 अक्टूबर 2026 से</span>':'');
      box.hidden=false;});
  });
})();

/* Puja samagri checklist: tap to tick, progress, saved on this device */
(function(){
  var apps=document.querySelectorAll('.sm-app');
  Array.prototype.forEach.call(apps,function(app){
    var key='sm:'+app.getAttribute('data-sm'),boxes=app.querySelectorAll('.sm-list input'),
        done=app.querySelector('[data-sm-done]'),fill=app.querySelector('[data-sm-fill]'),msg=app.querySelector('[data-sm-msg]'),
        saved={};
    try{saved=JSON.parse(localStorage.getItem(key)||'{}')||{}}catch(e){saved={}}
    function paint(save){
      var n=0,st={};
      Array.prototype.forEach.call(boxes,function(b){if(b.checked){n++;st[b.getAttribute('data-k')]=1}});
      if(done)done.textContent=n.toLocaleString('hi-IN');
      if(fill)fill.style.width=(boxes.length?Math.round(n/boxes.length*100):0)+'%';
      var all=boxes.length&&n===boxes.length;app.classList.toggle('is-done',!!all);if(msg)msg.hidden=!all;
      if(save){try{n?localStorage.setItem(key,JSON.stringify(st)):localStorage.removeItem(key)}catch(e){}}
    }
    Array.prototype.forEach.call(boxes,function(b){if(saved[b.getAttribute('data-k')])b.checked=true;b.addEventListener('change',function(){paint(true)})});
    var r=app.querySelector('[data-sm-reset]');
    if(r)r.addEventListener('click',function(){Array.prototype.forEach.call(boxes,function(b){b.checked=false});paint(true)});
    paint(false);
  });
})();

/* YouTube players we embed (live darshan, bhajans): start at 20% volume when the viewer unmutes. */
(function(){
  if(!window.MutationObserver)return;
  function vol(f){try{f.contentWindow.postMessage(JSON.stringify({event:'command',func:'setVolume',args:[20]}),'*');}catch(e){}}
  function fix(f){
    if(f._okbv||!/youtube(-nocookie)?\.com\/embed\//.test(f.src||''))return; f._okbv=1;
    if(f.src.indexOf('enablejsapi=1')<0)f.src=f.src+(f.src.indexOf('?')<0?'?':'&')+'enablejsapi=1';
    f.addEventListener('load',function(){[600,1500,3000,6000].forEach(function(ms){setTimeout(function(){vol(f)},ms)});});
  }
  [].forEach.call(document.querySelectorAll('iframe'),fix);
  new MutationObserver(function(ms){ms.forEach(function(m){[].forEach.call(m.addedNodes,function(n){
    if(n.tagName==='IFRAME')fix(n);else if(n.querySelectorAll)[].forEach.call(n.querySelectorAll('iframe'),fix);});});})
    .observe(document.documentElement,{childList:true,subtree:true});
})();
