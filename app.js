(function(){
var R=document.documentElement,base=document.body.dataset.base||'';
var tb=document.querySelector('.tema');if(tb)tb.onclick=function(){var t=R.dataset.theme==='oscuro'?'claro':'oscuro';R.dataset.theme=t;localStorage.setItem('tema',t)};
function fmt(f){if(!f)return'';var d=new Date(f);return d.toLocaleDateString('es-AR',{weekday:'short',day:'2-digit',month:'2-digit',timeZone:'America/Argentina/San_Luis'})+' '+d.toLocaleTimeString('es-AR',{hour:'2-digit',minute:'2-digit',timeZone:'America/Argentina/San_Luis'})}
function left(f){var s=(new Date(f)-Date.now())/1000;if(s<=0)return null;var d=Math.floor(s/86400),h=Math.floor(s%86400/3600),m=Math.floor(s%3600/60);return(d?d+' d ':'')+h+' h '+m+' min'}
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function link(x){return base+(x.pagina.indexOf('historia/')===0?'historia/index.html'+x.pagina.slice(8):x.pagina)}
// countdowns: tras la fecha se habilita el video
function tick(){document.querySelectorAll('.soon[data-fecha]').forEach(function(el){var l=left(el.dataset.fecha),c=el.querySelector('.countdown');if(l){c&&(c.textContent='Faltan '+l)}else if(el.dataset.yt&&!el.dataset.done){el.dataset.done=1;el.outerHTML='<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/'+el.dataset.yt+'" title="Video de YouTube" loading="lazy" allow="encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe></div>'}else if(c){c.textContent='¡Ya se estrenó! Buscalo en el canal.'}})}
tick();setInterval(tick,30000);
// share
document.querySelectorAll('.share').forEach(function(b){b.onclick=function(){var d={title:b.dataset.title,url:location.href};if(navigator.share)navigator.share(d).catch(function(){});else navigator.clipboard.writeText(location.href).then(function(){b.textContent='¡Enlace copiado!'})}});
// filtros portada
document.querySelectorAll('.chip').forEach(function(c){c.onclick=function(){document.querySelectorAll('.chip').forEach(function(o){o.classList.toggle('on',o===c);o.setAttribute('aria-pressed',o===c)});var f=c.dataset.f;document.querySelectorAll('#grid .card').forEach(function(k){k.hidden=!(f==='*'||k.dataset.tipo===f||k.dataset.estado===f)})}});
var needs=document.getElementById('proximos')||document.getElementById('db');if(!needs)return;
fetch(base+'data/videos.json').then(function(r){return r.json()}).then(function(D){var it=D.items;
var P=document.getElementById('proximos');
if(P){var up=it.filter(function(x){return x.estado==='programado'&&x.fecha&&new Date(x.fecha)>Date.now()}).sort(function(a,b){return a.fecha<b.fecha?-1:1});
P.innerHTML=up.length?up.map(function(x){var d=new Date(x.fecha);return'<li><span class="d">'+d.toLocaleDateString('es-AR',{day:'2-digit',timeZone:'America/Argentina/San_Luis'})+'<small>'+d.toLocaleDateString('es-AR',{month:'short',timeZone:'America/Argentina/San_Luis'})+'</small></span><span><a href="'+link(x)+'">'+esc(x.titulo)+'</a><br><span class="cd">'+fmt(x.fecha)+' · '+(x.tipo==='short'?'Short':x.tipo)+' · faltan '+left(x.fecha)+'</span></span></li>'}).join(''):'<li>No hay estrenos programados ahora. ¡Mirá el canal!</li>'}
var T=document.getElementById('db');if(!T)return;var key='fecha',dir=1,tb=T.querySelector('tbody');
var q=document.getElementById('q'),ft=document.getElementById('ft'),fm=document.getElementById('fm'),fe=document.getElementById('fe');
function draw(){var s=q.value.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'');
var r=it.filter(function(x){return(!ft.value||x.tipo===ft.value)&&(!fm.value||x.tema===fm.value)&&(!fe.value||x.estado===fe.value)&&(!s||(x.titulo+' '+x.tema+' '+x.tipo+' '+(x.serie||'')).toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').indexOf(s)>=0)});
r.sort(function(a,b){var A=a[key]||'~',B=b[key]||'~';return A<B?-dir:A>B?dir:0});
tb.innerHTML=r.map(function(x){return'<tr><td><a href="'+link(x)+'">'+esc(x.titulo)+'</a></td><td>'+x.tipo+'</td><td>'+x.tema+'</td><td><span class="badge '+x.estado+'">'+x.estado+'</span></td><td>'+(fmt(x.fecha)||'—')+'</td><td>'+(x.pdf?'<a href="'+base+x.pdf+'" download>PDF</a> ':'')+(x.youtube_url&&x.estado==='publicado'?'<a href="'+x.youtube_url+'" rel="noopener">YouTube</a>':'')+'</td></tr>'}).join('');
document.getElementById('cnt').textContent=r.length+' de '+it.length+' elementos'}
[q,ft,fm,fe].forEach(function(el){el.addEventListener('input',draw)});
T.querySelectorAll('th button').forEach(function(b){b.onclick=function(){dir=key===b.dataset.k?-dir:1;key=b.dataset.k;draw()}});draw();
}).catch(function(){var P=document.getElementById('proximos');if(P)P.innerHTML='<li>No se pudo cargar el calendario.</li>'});
})();
