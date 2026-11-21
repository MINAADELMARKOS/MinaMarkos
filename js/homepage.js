/* Dependency-free homepage navigation and project filtering. */
(() => {
  'use strict';
  const toggle=document.querySelector('.navbar-toggler');
  const menu=document.querySelector('#navbarSupportedContent');
  if(toggle&&menu){
    document.documentElement.classList.add('navigation-ready');
    toggle.hidden=false;
    const close=()=>{menu.classList.remove('show');toggle.setAttribute('aria-expanded','false');};
    toggle.addEventListener('click',()=>{
      const open=toggle.getAttribute('aria-expanded')!=='true';
      menu.classList.toggle('show',open);toggle.setAttribute('aria-expanded',String(open));
    });
    matchMedia('(min-width: 992px)').addEventListener('change',close);
    toggle.addEventListener('keydown',event=>{if(event.key==='Escape')close();});
    menu.addEventListener('click',event=>{if(event.target.closest('a'))close();});
    menu.addEventListener('keydown',event=>{if(event.key==='Escape'){close();toggle.focus();}});
  }
  const filters=document.querySelector('.portfolio-filter');
  const cards=[...document.querySelectorAll('.portfolio-grid > .all')];
  if(filters&&cards.length){
    filters.hidden=false;
    filters.addEventListener('click',event=>{
      const button=event.target.closest('[data-filter]');if(!button)return;
      const selector=button.dataset.filter;
      filters.querySelectorAll('[data-filter]').forEach(b=>{const active=b===button;b.setAttribute('aria-pressed',String(active));b.closest('li').classList.toggle('active',active);});
      cards.forEach(card=>{card.hidden=selector!=='*'&&!card.matches(selector);});
      const status=document.querySelector('#project-filter-status');
      if(status)status.textContent=`${cards.filter(c=>!c.hidden).length} projects shown`;
    });
  }
})();
