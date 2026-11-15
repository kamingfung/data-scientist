// Optional interactivity, inlined by page() only when a slide uses it.
// Hover tooltips on [data-tip] marks and on numbers with [data-src] (shows the source);
// click-to-expand detail panels (.xp-btn + .xp-panel), copied onto their own print page;
// scenario toggles (.tabs). Keys and clicks on these controls never move the slide.
(function(){
const tip=document.createElement('div');tip.className='tip';tip.hidden=true;document.body.appendChild(tip);
const mark=e=>e.target.closest&&e.target.closest('[data-tip],[data-src]');
document.addEventListener('pointerover',e=>{const t=mark(e);if(t){tip.textContent=t.dataset.tip||('Source: '+t.dataset.src);tip.hidden=false;}});
document.addEventListener('pointermove',e=>{if(!tip.hidden){tip.style.left=Math.max(8,Math.min(e.clientX+14,innerWidth-tip.offsetWidth-8))+'px';tip.style.top=(e.clientY+18)+'px';}});
document.addEventListener('pointerout',e=>{if(mark(e))tip.hidden=true;});
const guard=el=>{el.addEventListener('click',e=>e.stopPropagation());el.addEventListener('keydown',e=>{if(e.key===' '||e.key==='Enter'||e.key==='Escape')e.stopPropagation();});};
const btns=[...document.querySelectorAll('.xp-btn')];
const set=(b,o)=>{b.setAttribute('aria-expanded',o);document.getElementById(b.getAttribute('aria-controls')).hidden=!o;};
btns.forEach(b=>{const p=document.getElementById(b.getAttribute('aria-controls')),s=p.closest('.slide'),host=s.closest('.wrap')||s;
  const c=document.createElement('div');c.className='xp-print '+(p.classList.contains('corr')?'corr':'');c.innerHTML=p.innerHTML;host.after(c);
  p.tabIndex=-1;guard(b);guard(p);
  b.addEventListener('click',()=>{const o=b.getAttribute('aria-expanded')!=='true';set(b,o);if(o)p.focus();});
  p.addEventListener('keydown',e=>{if(e.key==='Escape'){set(b,false);b.focus();}});});
const closeAll=()=>btns.forEach(b=>set(b,false));
document.addEventListener('click',closeAll);document.addEventListener('keydown',e=>{if(e.key==='Escape')closeAll();});
document.querySelectorAll('.tabs').forEach(t=>{const bs=[...t.querySelectorAll('.tab-bar button')],ps=[...t.querySelectorAll('.tab-panel')];
  bs.forEach((b,i)=>{guard(b);b.addEventListener('click',()=>{bs.forEach((x,j)=>x.setAttribute('aria-selected',i===j));ps.forEach((p,j)=>p.hidden=i!==j);});});});
})();
