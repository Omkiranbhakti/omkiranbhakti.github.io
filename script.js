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
      20261016:'r32U54qyerw',20261017:'FFcNanFHSaY',20261018:'G99-49Pfs6U',20261019:'G99-49Pfs6U',20261020:'pCixItfj5Vo'};
    var weekArt=[['pCixItfj5Vo',80,'जय श्री राम'],['Kbe3pbLsg1U',80,'हर हर महादेव'],['707iS1Iyv-E',12,'जय बजरंगबली'],['NGI-JiRiwSc',80,'गणपति बप्पा मोरया'],
      ['pCixItfj5Vo',80,'ॐ नमो नारायणाय'],['2yVR5zSaKpc',76,'जय माता दी'],['707iS1Iyv-E',12,'जय बजरंगबली']];
    var art=document.querySelector('#today-art img'), cap=document.getElementById('today-cap');
    function setArt(id,pos,c){if(!art)return;art.onerror=function(){art.onerror=null;art.src='https://i.ytimg.com/vi/'+id+'/hqdefault.jpg'};
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
})();
