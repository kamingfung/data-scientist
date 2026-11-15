// Wrap and scale slides, stamp "n / N" in each footer,
// arrow keys / PageUp / PageDown / Space or scrolling to move, #n opens slide n,
// F or P toggles presentation mode.
const slides=[...document.querySelectorAll('.slide')];slides.forEach(s=>{const w=document.createElement('div');w.className='wrap';s.replaceWith(w);w.appendChild(s);});
function fit(){const s=Math.min(1,(window.innerWidth-48)/1280);document.querySelector('.deck').style.setProperty('--s',s);}fit();window.addEventListener('resize',fit);slides.forEach((s,i)=>s.querySelector('footer').setAttribute('data-n',(i+1)+' / '+slides.length));
let i=0,present=false;function show(k){i=(k+slides.length)%slides.length;slides.forEach((s,j)=>s.parentElement.classList.toggle('on',j===i));if(!present)slides[i].parentElement.scrollIntoView({behavior:'smooth'});}
document.addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key==='PageDown'||e.key===' ')show(i+1);else if(e.key==='ArrowLeft'||e.key==='PageUp')show(i-1);else if(e.key==='f'||e.key==='p'){present=!present;document.body.classList.toggle('present',present);show(i);}});
document.querySelectorAll('.slide').forEach((s,j)=>s.addEventListener('click',()=>{if(present)show(j+1);}));
// keep the arrow keys in step with scrolling; #n opens slide n
window.addEventListener('scroll',()=>{if(present)return;let b=0,d=Infinity;slides.forEach((s,j)=>{const r=s.parentElement.getBoundingClientRect(),t=Math.abs(r.top+r.height/2-innerHeight/2);if(t<d){d=t;b=j;}});i=b;},{passive:true});
const hash=/^#(\d+)$/.exec(location.hash);if(hash){i=Math.min(slides.length,+hash[1])-1;slides[i].parentElement.scrollIntoView();}
// optional correction popups; no-op without .corr-badge
document.querySelectorAll('.corr-badge').forEach(b=>{const p=document.getElementById(b.getAttribute('aria-controls'));const set=o=>{b.setAttribute('aria-expanded',o);p.hidden=!o;if(o)p.focus();};p.tabIndex=-1;b.addEventListener('click',e=>{e.stopPropagation();set(b.getAttribute('aria-expanded')!=='true');});b.addEventListener('keydown',e=>{if(e.key===' '||e.key==='Enter')e.stopPropagation();});p.addEventListener('click',e=>e.stopPropagation());p.addEventListener('keydown',e=>{if(e.key==='Escape'){set(false);b.focus();}e.stopPropagation();});});
const closeAll=()=>document.querySelectorAll('.corr-badge[aria-expanded=true]').forEach(b=>{b.setAttribute('aria-expanded','false');document.getElementById(b.getAttribute('aria-controls')).hidden=true;});
document.addEventListener('click',closeAll);document.addEventListener('keydown',e=>{if(e.key==='Escape')closeAll();});
