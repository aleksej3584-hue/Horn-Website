(function(){
  var doc=document.documentElement, body=document.body;

  /* ---------- entrance ---------- */
  function reveal(){doc.classList.remove('intro');}
  if(doc.classList.contains('intro')){
    var go=function(){requestAnimationFrame(function(){requestAnimationFrame(reveal);});};
    if(document.fonts&&document.fonts.ready){document.fonts.ready.then(go,go);}else{go();}
    setTimeout(reveal,900);
  }

  /* ---------- header state ---------- */
  var head=document.querySelector('.site-head');
  function onScroll(){if(head)head.classList.toggle('scrolled',window.scrollY>8);}
  onScroll();
  window.addEventListener('scroll',onScroll,{passive:true});

  /* ---------- mobile menu ---------- */
  var burger=document.querySelector('.burger'), menu=document.getElementById('menu');
  if(burger&&menu){
    var accs=[].slice.call(menu.querySelectorAll('.acc'));
    var setAcc=function(acc,open){acc.classList.toggle('open',open);acc.querySelector('button').setAttribute('aria-expanded',open?'true':'false');};
    var setMenu=function(open){
      body.classList.toggle('nav-open',open);
      burger.setAttribute('aria-expanded',open?'true':'false');
      burger.setAttribute('aria-label',open?'Menü schließen':'Menü öffnen');
      menu.setAttribute('aria-hidden',open?'false':'true');
      if(open){menu.removeAttribute('inert');}else{menu.setAttribute('inert','');accs.forEach(function(a){setAcc(a,false);});}
    };
    burger.addEventListener('click',function(){setMenu(!body.classList.contains('nav-open'));});
    accs.forEach(function(acc){
      acc.querySelector('button').addEventListener('click',function(){
        var willOpen=!acc.classList.contains('open');
        accs.forEach(function(a){setAcc(a,false);});
        setAcc(acc,willOpen);
      });
    });
    menu.addEventListener('click',function(e){if(e.target.closest('a'))setMenu(false);});
    document.addEventListener('keydown',function(e){
      if(e.key==='Escape'&&body.classList.contains('nav-open')){setMenu(false);burger.focus();}
    });
    var desk=matchMedia('(min-width:1024px)');
    var onDesk=function(){if(desk.matches)setMenu(false);};
    desk.addEventListener?desk.addEventListener('change',onDesk):desk.addListener(onDesk);
  }

  /* ---------- year ---------- */
  [].forEach.call(document.querySelectorAll('[data-year]'),function(el){el.textContent=new Date().getFullYear();});

  /* ---------- contact form: composes an e-mail ---------- */
  var form=document.getElementById('anfrage');
  if(form){
    var topic=form.querySelector('#f-thema');
    var m=/[?&]thema=([^&#]+)/.exec(location.search);
    if(m&&topic){
      var val=decodeURIComponent(m[1]);
      [].forEach.call(topic.options,function(o){if(o.value===val)topic.value=val;});
    }
    var msg=form.querySelector('.form-msg');
    var setErr=function(el,text){
      var err=document.getElementById(el.id+'-err');
      el.setAttribute('aria-invalid',text?'true':'false');
      if(err)err.textContent=text||'';
    };
    form.addEventListener('submit',function(e){
      e.preventDefault();
      var name=form.querySelector('#f-name'), contact=form.querySelector('#f-kontakt'),
          place=form.querySelector('#f-ort'), text=form.querySelector('#f-msg'), ok=form.querySelector('#f-ds');
      var first=null;
      [[name,'Bitte geben Sie Ihren Namen an.'],[contact,'Bitte geben Sie eine Telefonnummer oder E-Mail-Adresse an.'],[text,'Bitte beschreiben Sie kurz Ihr Anliegen.']].forEach(function(p){
        var bad=!p[0].value.trim();
        setErr(p[0],bad?p[1]:'');
        if(bad&&!first)first=p[0];
      });
      var dsErr=document.getElementById('f-ds-err');
      if(!ok.checked){if(dsErr)dsErr.textContent='Bitte bestätigen Sie den Hinweis zum Datenschutz.';if(!first)first=ok;}
      else if(dsErr){dsErr.textContent='';}
      if(first){first.focus();msg.textContent='';return;}

      var thema=topic.options[topic.selectedIndex].text;
      var lines=['Name: '+name.value.trim(),'Kontakt: '+contact.value.trim()];
      if(place.value.trim())lines.push('Ort des Projekts: '+place.value.trim());
      lines.push('Thema: '+thema,'',text.value.trim());
      var href='mailto:info@horn-elektro.de?subject='+encodeURIComponent('Anfrage: '+thema)+'&body='+encodeURIComponent(lines.join('\n'));
      msg.textContent='Ihr E-Mail-Programm öffnet sich mit der fertigen Nachricht. Falls nicht: Schreiben Sie uns direkt an info@horn-elektro.de oder rufen Sie 040 – 700 61 01 an.';
      window.location.href=href;
    });
    ['#f-name','#f-kontakt','#f-msg'].forEach(function(sel){
      var el=form.querySelector(sel);
      el.addEventListener('input',function(){if(el.value.trim())setErr(el,'');});
    });
  }
})();
