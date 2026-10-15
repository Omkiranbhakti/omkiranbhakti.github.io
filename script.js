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
      ['रविवार','सूर्य देव','आज सूर्य देव की उपासना का दिन है। सूर्य बीज मंत्र का जाप करें।','aarti-mantra.html','मंत्र संग्रह देखें'],
      ['सोमवार','भगवान शिव','सोमवार भोलेनाथ का दिन है। शिव आरती और शिव चालीसा का पाठ करें।','shiv-aarti-om-jai-shiv-omkara.html','शिव आरती पढ़ें'],
      ['मंगलवार','हनुमान जी','मंगलवार बजरंगबली का दिन है। हनुमान चालीसा का पाठ करें।','hanuman-chalisa.html','हनुमान चालीसा पढ़ें'],
      ['बुधवार','श्री गणेश','बुधवार विघ्नहर्ता गणेश जी का दिन है। गणेश आरती गाएँ।','ganesh-aarti-jai-ganesh-deva.html','गणेश आरती पढ़ें'],
      ['गुरुवार','भगवान विष्णु','गुरुवार श्रीहरि विष्णु का दिन है। ॐ जय जगदीश हरे आरती गाएँ।','om-jai-jagdish-hare-aarti.html','जगदीश आरती पढ़ें'],
      ['शुक्रवार','माता रानी','शुक्रवार देवी माँ का दिन है। माता रानी के भजन सुनें।','mata-rani-bhajan.html','माता रानी भजन'],
      ['शनिवार','शनि देव और हनुमान जी','शनिवार को शनि देव और हनुमान जी का स्मरण किया जाता है।','hanuman-chalisa.html','हनुमान चालीसा पढ़ें']];
    var w=week[ist.getDay()], h=today.querySelector('h2'), p=today.querySelector('p.say'), a=today.querySelector('a.go'), when=today.querySelector('.when');
    if(navratri[ymd]){when.textContent='आज · शारदीय नवरात्रि 2026';h.textContent=navratri[ymd];
      p.textContent='नवरात्रि के हर दिन देवी के एक स्वरूप की पूजा होती है। आज की आरती और पूरे नौ दिनों की सूची देखें।';a.href='navratri-2026.html';a.textContent='नवरात्रि 2026 पेज खोलें';}
    else{when.textContent='आज '+w[0];h.textContent=w[1];p.textContent=w[2];a.href=w[3];a.textContent=w[4];}
  }

  // Navratri page: highlight today
  document.querySelectorAll('.days li[data-ymd]').forEach(function(li){
    var d=new Date(), ist=new Date(d.getTime()+(d.getTimezoneOffset()+330)*60000);
    var ymd=String(ist.getFullYear()*10000+(ist.getMonth()+1)*100+ist.getDate());
    if(li.dataset.ymd.split(',').indexOf(ymd)>-1){li.classList.add('now');li.insertAdjacentHTML('afterbegin','<strong style="color:var(--sindoor)">आज</strong> ');}
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
})();
