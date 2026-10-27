import json,re,subprocess,os,html
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
B='https://admgrow.github.io/arte-experimental-v5x/'
CH='https://www.youtube.com/@Arteexperimentalv5x'
import functools
@functools.lru_cache(None)
def pages(pdf):
    n=int(re.search(r'Pages:\s+(\d+)',subprocess.run(['pdfinfo',pdf],capture_output=True,text=True).stdout)[1])
    return [subprocess.run(['pdftotext','-f',str(i),'-l',str(i),pdf,'-'],capture_output=True,text=True).stdout.replace('ﬁ','fi').replace('ﬂ','fl') for i in range(1,n+1)]
NOISE=re.compile(r'^(Arte experimental v5x|ARTE EXPERIMENTAL V5X|SUSCRIBITE|Gris oscuro.*|Celeste:.*|Dibujo terminado|HB|2B|\d)$',re.I)
def blocks(t):
    out=[]
    for b in re.split(r'\n\s*\n',t):
        ls=[l.strip() for l in b.split('\n') if l.strip() and not NOISE.match(l.strip())]
        if ls: out.append(ls)
    return out
def parse_tut(pdf):
    steps=[];mat=[];tips=[];
    for i,t in enumerate(pages(pdf),1):
        bl=blocks(t)
        if not bl: continue
        head=bl[0][0]
        if re.match(r'PASOS? ',head,re.I):
            rest=bl[0][1:]; others=bl[1:]
            if not rest and others: rest=others.pop(0)
            title=rest[0] if rest else ''
            desc=' '.join([l for l in rest[1:] if not l.startswith('Herramienta')]+[' '.join(x) for x in others if not x[0].startswith('Herramienta')])
            tool=next((l for x in bl for l in x if l.startswith('Herramienta')),'')
            steps.append(dict(label=head.capitalize(),title=title,desc=desc.strip(),tool=tool,page=i))
        elif 'ANTES DE ARRANCAR' in head or any('Materiales' in x[0] for x in bl):
            mat=[' '.join(x) for x in bl if x[0] not in('ANTES DE ARRANCAR',)]
        elif re.search(r'CONSEJO|ERRORES',t,re.I) and i>2:
            tips=[' '.join(x) for x in bl]
    return steps,mat,tips
T=[('01','gato','Cómo dibujar un gato fácil con lápiz','animal','B-dhUzr_28Y',None,'publicado'),
('02','pato','Cómo dibujar un pato con marcador','animal','D36bi5JCMKY',None,'publicado'),
('03','estrella','Cómo dibujar una estrella con fibras','animal','H6GIoIHenek',None,'publicado'),
('04','pez','Cómo dibujar un pez con birome','animal','C1FRxqEXmPk','2026-10-27','programado'),
('05','caracol','Cómo dibujar un caracol con marcador','insecto','rIliGBPQLhI','2026-10-28','programado'),
('06','perrito','Cómo dibujar un perrito kawaii con fibras','animal','tXH91Qugvtc','2026-10-29','programado'),
('07','conejo','Cómo dibujar un conejo de una sola línea','animal','tlio24sl6_A','2026-10-30','programado'),
('08','buho','Cómo dibujar un búho con lápiz y sombreado','animal','uhTSJnwXiv4','2026-10-31','programado'),
('09','tortuga','Cómo dibujar una tortuga con crayones','animal','Kozza5oHPfg','2026-11-01','programado'),
('10','pinguino','Cómo dibujar un pingüino con marcador y relleno plano','animal','7BEKPFmi9sY','2026-11-02','programado'),
('11','zorro','Cómo dibujar un zorro con acuarela','animal','lzC0j1ICisE','2026-11-03','programado'),
('12','elefante','Cómo dibujar un elefante con lápiz realista','animal','aq2IBz58shw','2026-11-04','programado'),
('13','osito','Cómo dibujar un osito kawaii con lápices de colores','animal','F3XQyZxVVHs','2026-11-05','programado')]
H=[('Dadaísmo','Movimiento surgido en Zúrich en 1916, en torno al Cabaret Voltaire, que cuestionó la lógica y las convenciones del arte.'),
('Surrealismo','Movimiento iniciado en París en 1924 con el primer Manifiesto de André Breton; exploró los sueños y el inconsciente.'),
('Futurismo','Movimiento italiano lanzado en 1909 con el manifiesto de Filippo Tommaso Marinetti, fascinado por la velocidad y la máquina.'),
('Constructivismo','Corriente rusa de la década de 1910-1920 que unió arte, geometría, materiales industriales y diseño.'),
('Expresionismo abstracto','Pintura de posguerra centrada en Nueva York (décadas de 1940-1950), con gesto, color y gran formato.'),
('Arte cinético y op art','Obras que se mueven de verdad o que generan ilusión de movimiento con patrones ópticos.'),
('Pop art','Arte de las décadas de 1950-1960 que tomó imágenes de la publicidad, los cómics y el consumo masivo.'),
('Fluxus y arte conceptual','Prácticas de las décadas de 1960-1970 donde la idea, la acción o la instrucción importan más que el objeto.'),
('Videoarte','Uso del video y la televisión como medio artístico a partir de la década de 1960.'),
('Land art','Obras hechas en el paisaje y con materiales de la naturaleza, desde fines de la década de 1960.'),
('Arte generativo y digital','Obras creadas con reglas, algoritmos y computadoras, desde los primeros gráficos por computadora de la década de 1960.'),
('Arte con IA','Prácticas recientes que usan sistemas de inteligencia artificial como herramienta o tema de la obra.')]
V=[]
for n,s,t,tema,yt,f,e in T:
    st,mat,tips=parse_tut(f'pdf/tutorial-{n}-{s}.pdf')
    V.append(dict(id=f'tutorial-{n}-{s}',tipo='tutorial' if e=='publicado' else 'short',titulo=t,tema=tema,estado=e,
      fecha=(f+'T12:00:00-03:00') if f else None,youtube_id=yt,youtube_url=f'https://youtu.be/{yt}',
      pagina=f'tutoriales/{n}-{s}.html',pdf=f'pdf/tutorial-{n}-{s}.pdf',imagen=f'img/p/tutorial-{n}-{s}-1.webp',
      paginas_pdf=len(pages(f'pdf/tutorial-{n}-{s}.pdf')),_steps=st,_mat=mat,_tips=tips,serie='Tutoriales de dibujo'))
for slug,t,np_ in [('casita','Molde de casita de papel',2),('robot-bulon','Molde de robot Bulón',3)]:
    V.append(dict(id=f'molde-{slug}',tipo='molde',titulo=t,tema='molde',estado='pendiente',fecha=None,youtube_id=None,youtube_url=None,
      pagina=f'moldes/{slug}.html',pdf=f'pdf/molde-{slug}.pdf',imagen=f'img/p/molde-{slug}-1.webp',paginas_pdf=np_,serie='Moldes',nota='Video próximamente'))
for i,(t,r) in enumerate(H,1):
    V.append(dict(id=f'historia-{i:02d}',tipo='historia',titulo=f'Historia del arte experimental #{i}: {t}',tema='historia',
      estado='programado' if i<=2 else 'pendiente',fecha=f'2026-10-{26+i}T18:00:00-03:00' if i<=2 else None,youtube_id=None,youtube_url=None,
      pagina=f'historia/#ep{i}',pdf=None,imagen=f'img/historia/ep{i:02d}.svg',resumen=r,serie='Historia del arte experimental'))
pub=[{k:v for k,v in x.items() if not k.startswith('_')} for x in V]
os.makedirs('data',exist_ok=True)
json.dump(dict(canal='Arte experimental v5x',handle='@Arteexperimentalv5x',url_canal=CH,actualizado='2026-10-26',
  zona_horaria='America/Argentina (GMT-3)',nota='Fuente única del sitio. Sin métricas.',items=pub),open('data/videos.json','w'),ensure_ascii=False,indent=1)
# ---------- historia svgs (propias) ----------
os.makedirs('img/historia',exist_ok=True)
import random
pal=['#e4572e','#f3a712','#29335c','#669bbc','#a8c686','#db2763','#12355b','#ffd23f']
for i in range(1,13):
    random.seed(i*7);s=''
    for k in range(9):
        c=random.choice(pal);x,y=random.randint(0,300),random.randint(0,170);w=random.randint(30,140)
        s+=random.choice([f'<circle cx="{x}" cy="{y}" r="{w//2}" fill="{c}" opacity=".85"/>',f'<rect x="{x}" y="{y}" width="{w}" height="{w//2}" fill="{c}" opacity=".85" transform="rotate({random.randint(-30,30)} {x} {y})"/>',f'<path d="M{x} {y} q{w} -{w} {w*2} 0" stroke="{c}" stroke-width="9" fill="none"/>'])
    open(f'img/historia/ep{i:02d}.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 180"><rect width="320" height="180" fill="#fff6e8"/>{s}<text x="16" y="164" font-family="sans-serif" font-size="34" font-weight="700" fill="#1d1d1f">#{i}</text></svg>')
# ---------- layout ----------
def e(x):return html.escape(x or '',quote=True)
def page(path,title,desc,body,ld=None,img=None):
    d='../'*path.count('/')
    lds=f'<script type="application/ld+json">{json.dumps(ld,ensure_ascii=False)}</script>' if ld else ''
    url=B+re.sub(r'index\.html$','',path)
    og=f'<meta property="og:image" content="{B}{img}">' if img else ''
    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} · Arte experimental v5x</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">{og}
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Roboto:wght@400;700&display=swap"><link rel="stylesheet" href="{d}style.css"><script>document.documentElement.dataset.theme=localStorage.getItem('tema')||(matchMedia('(prefers-color-scheme: dark)').matches?'oscuro':'claro')</script>{lds}</head>
<body data-base="{d}"><a class="skip" href="#main">Saltar al contenido</a>
<header class="top"><a class="logo" href="{d}index.html"><span aria-hidden="true">✎</span> Arte experimental <b>v5x</b></a>
<nav aria-label="Principal"><a href="{d}tutoriales/index.html">Tutoriales</a><a href="{d}moldes/index.html">Moldes</a><a href="{d}historia/index.html">Historia</a><a href="{d}base-de-datos/index.html">Base de datos</a><a href="{d}blog/index.html">Blog</a><a href="{CH}" rel="noopener">YouTube</a>
<button class="tema" type="button" aria-label="Cambiar modo claro/oscuro">◐</button></nav></header>
<main id="main">{body}</main>
<footer>Arte experimental v5x · <a href="{CH}" rel="noopener">Canal de YouTube</a> · Licencia de descargas: uso personal libre; no reventa.</footer>
<script src="{d}app.js" defer></script></body></html>'''
def fmt(f):
    if not f:return ''
    y,m,dd=f[:10].split('-');return f'{dd}/{m}/{y}'+(' · '+f[11:16]+' (GMT-3)' if len(f)>10 else '')
def badge(x):return f'<span class="badge {x["estado"]}">{x["estado"]}</span>'
def video_block(x):
    if x['estado']=='publicado':
        return f'<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/{x["youtube_id"]}" title="{e(x["titulo"])} (YouTube)" loading="lazy" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture; fullscreen" allowfullscreen></iframe></div>'
    if x['estado']=='programado' and x.get('youtube_id'):
        return f'<div class="soon" data-fecha="{x["fecha"]}" data-yt="{x["youtube_id"]}"><p><b>Estreno:</b> {fmt(x["fecha"])}</p><p class="countdown" aria-live="polite"></p></div>'
    if x['estado']=='programado': return f'<div class="soon" data-fecha="{x["fecha"]}"><p><b>Estreno:</b> {fmt(x["fecha"])}</p><p class="countdown"></p></div>'
    return '<div class="soon"><p>Video próximamente.</p></div>'

# ---------- capturas de diapositivas (páginas reales de los PDF de Google Slides) ----------
SM=json.load(open('data/slides-moldes.json'))
NOISE2=re.compile(r'^(ARTE EXPERIMENTAL V5X|@Arteexperimentalv5x|Arte experimental v5x)$',re.I)
def sl_title(pdf,i):
    t=pages(pdf)[i-1];ls=[l.strip() for l in t.split('\n') if l.strip() and not NOISE2.match(l.strip()) and not NOISE.match(l.strip())]
    return ' · '.join(ls[:2])
def deck_of(key):
    """key: tutorial-01-gato | molde-casita | molde-casita-video | molde-robot-bulon-video -> lista (src,w,h,caption)"""
    if key in SM:
        dn={'molde-casita-video':'Slides del video del molde de casita (Short 9:16)','molde-robot-bulon-video':'Slides del video del molde Bulón (Largo 16:9)'}[key]
        return [(f'img/slides/{key}-{d["n"]}.webp',d['w'],d['h'],f'{dn}, diapositiva {d["n"]}: {d["t"]}') for d in SM[key]]
    pdf=f'pdf/{key}.pdf';n=len(pages(pdf))
    dn=('Slides del tutorial '+key[9:11]+' ('+key[12:]+')') if key.startswith('tutorial') else ('Molde A4 '+key[6:]+', hoja')
    from PIL import Image as _I
    def sz(i):return _I.open(f'img/p/{key}-{i}.webp').size
    return [(f'img/p/{key}-{i}.webp',*sz(i),f'{dn} {i} de {n}: {sl_title(pdf,i)}' if key.startswith('molde') else f'{dn}, diapositiva {i} de {n}: {sl_title(pdf,i)}') for i in range(1,n+1)]
def fig(src,w,h,cap,d):return f'<figure><a href="{d}{src}"><img src="{d}{src}" alt="{e(cap)}" loading="lazy" width="{w}" height="{h}"></a><figcaption>{e(cap)}</figcaption></figure>'
def gallery(key,d,only=None,title=None):
    items=deck_of(key)
    if only: items=[items[i-1] for i in only if i<=len(items)] if not key in SM else [x for x in items if int(x[0].rsplit('-',1)[1][:-5]) in only]
    v=' v' if items and items[0][2]>items[0][1] else ''
    return (f'<h2 class="gal-h">{e(title)}</h2>' if title else '')+f'<div class="gal{v}">'+''.join(fig(*x,d) for x in items)+'</div>'
def slide_codes(body,d):
    body=re.sub(r'\{SLIDE:([\w-]+):(\d+)\}',lambda m:(lambda it:fig(*it,d) if it else '')(next((x for x in deck_of(m[1]) if re.search(rf'-{m[2]}\.webp$',x[0])),None)),body)
    body=re.sub(r'\{GAL:([\w-]+)(?::([\d,]+))?\}',lambda m:gallery(m[1],d,[int(i) for i in m[2].split(',')] if m[2] else None),body)
    return body
def share(t):return f'<button class="btn ghost share" type="button" data-title="{e(t)}">Compartir</button>'
# ---------- tutorials ----------
tuts=[x for x in V if x['id'].startswith('tutorial')]
GEN_TIPS=['Bocetá suave primero: las líneas de guía se borran al final.','Si algo no sale, pausá el video o volvé a la diapositiva del PDF.','Practicá el dibujo dos o tres veces: la segunda siempre sale mejor.']
for k,x in enumerate(tuts):
    p=x['pagina'];base=x['pdf'][4:-4]
    steps=''.join(f'<li class="step"><figure><img src="../img/p/{base}-{s["page"]}.webp" alt="{e(s["label"]+": "+s["title"])}" loading="lazy" width="760" height="428"></figure><div><h3>{e(s["label"])} · {e(s["title"])}</h3><p>{e(s["desc"])}</p>{f"<p class=tool>{e(s[chr(116)+chr(111)+chr(111)+chr(108)])}</p>" if s["tool"] else ""}</div></li>' for s in x['_steps'])
    mat=''.join(f'<li>{e(m)}</li>' for m in x['_mat'] if m!='Materiales') or '<li>Ver diapositiva de materiales en el PDF.</li>'
    tips=''.join(f'<li>{e(t)}</li>' for t in (x['_tips'][2:] if x['_tips'] and x['_tips'][0].isupper() else x['_tips']) if len(t)>14) or ''.join(f'<li>{t}</li>' for t in GEN_TIPS)
    thumb=f'https://i.ytimg.com/vi/{x["youtube_id"]}/hqdefault.jpg' if x['estado']=='publicado' else None
    prev=tuts[k-1] if k else None;nxt=tuts[k+1] if k+1<len(tuts) else None
    nav='<nav class="pn" aria-label="Anterior y siguiente">'+(f'<a href="{prev["pagina"][11:]}">← {e(prev["titulo"])}</a>' if prev else '<span></span>')+(f'<a href="{nxt["pagina"][11:]}">{e(nxt["titulo"])} →</a>' if nxt else '')+'</nav>'
    howto={"@type":"HowTo","name":x['titulo'],"image":B+x['imagen'],"tool":[{"@type":"HowToTool","name":m} for m in x['_mat'][1:3]],
      "step":[{"@type":"HowToStep","name":s['title'],"text":s['desc'] or s['title'],"image":B+f'img/p/{base}-{s["page"]}.webp'} for s in x['_steps']]}
    ld=[dict(howto,**{"@context":"https://schema.org"})]
    if x['estado']=='publicado':
        ld.append({"@context":"https://schema.org","@type":"VideoObject","name":x['titulo'],"description":f"{x['titulo']}: tutorial paso a paso del canal Arte experimental v5x.","thumbnailUrl":thumb,"embedUrl":f"https://www.youtube-nocookie.com/embed/{x['youtube_id']}","contentUrl":x['youtube_url']})
    hero=f'<img class="cover" src="{thumb or "../"+x["imagen"]}" alt="Miniatura: {e(x["titulo"])}" width="480" height="360">'
    body=f'''<article class="post"><p class="crumbs"><a href="index.html">Tutoriales</a> › {e(x["titulo"])}</p>
<div class="post-head">{hero}<div><p class="kicker">Tutorial {x["id"][9:11]} · {"Video" if x["tipo"]=="tutorial" else "Short"} {badge(x)}</p><h1>{e(x["titulo"])}</h1>
<p>Dibujo paso a paso con {len(x["_steps"])} bloques de pasos explicados abajo. Mirá el video, descargá las diapositivas en PDF ({x["paginas_pdf"]} páginas) y practicá a tu ritmo.</p>
<p class="actions"><a class="btn" href="../{x["pdf"]}" download>⬇ Descargar slides (PDF)</a> {f'<a class="btn ghost" href="{x["youtube_url"]}" rel="noopener">Ver en YouTube</a>' if x["estado"]=="publicado" else ""} {share(x["titulo"])}</p></div></div>
<h2>Video</h2>{video_block(x)}
<h2>Materiales</h2><ul class="mat">{mat}</ul>
<h2>Paso a paso</h2><ol class="steps">{steps}</ol>
<h2>Consejos</h2><ul class="tips">{tips}</ul>
{gallery(base,"../",title="Todas las diapositivas del tutorial")}
<p class="lic">Las imágenes de los pasos son páginas del PDF del tutorial (material propio del canal). Licencia: uso personal libre; no reventa.</p>
{nav}</article>'''
    open(p,'w').write(page(p,x['titulo'],f'{x["titulo"]}: paso a paso explicado, video y slides en PDF para descargar.',body,ld,x['imagen']))
def card(x,d=''):
    img=f'https://i.ytimg.com/vi/{x["youtube_id"]}/hqdefault.jpg' if x['estado']=='publicado' else d+x['imagen']
    link=d+x['pagina'] if not x['pagina'].startswith('historia') else d+'historia/index.html#'+x['pagina'].split('#')[1]
    dl=f'<a class="btn sm" href="{d}{x["pdf"]}" download>⬇ PDF</a>' if x.get('pdf') else ''
    return f'<article class="card" data-tipo="{x["tipo"]}" data-tema="{x["tema"]}" data-estado="{x["estado"]}"><a href="{link}"><img src="{img}" alt="" loading="lazy" width="480" height="300"></a><div class="cb">{badge(x)} <span class="tag">{x["tipo"]}</span><h3><a href="{link}">{e(x["titulo"])}</a></h3><p class="date">{fmt(x["fecha"]) or ("Video próximamente" if x["tipo"]=="molde" else "")}</p>{dl}</div></article>'
filt='''<div class="filters" role="group" aria-label="Filtrar"><button class="chip on" data-f="*">Todo</button><button class="chip" data-f="tutorial">Videos</button><button class="chip" data-f="short">Shorts</button><button class="chip" data-f="molde">Moldes</button><button class="chip" data-f="historia">Historia</button><button class="chip" data-f="publicado">Publicados</button><button class="chip" data-f="programado">Programados</button></div>'''
dlall='<a class="btn" href="descargas/arte-experimental-v5x-slides-y-moldes.zip" download>⬇ Descargar todos (ZIP, 15 PDFs)</a>'
home=f'''<section class="hero"><div class="blob b1"></div><div class="blob b2"></div><div class="hero-in"><p class="kicker">Canal de YouTube · @Arteexperimentalv5x</p>
<h1>Dibujá, recortá y experimentá</h1><p class="lead">Tutoriales de dibujo paso a paso, moldes de papel para imprimir y una serie sobre la historia del arte experimental. Todo con slides en PDF para descargar gratis.</p>
<p class="actions">{dlall} <a class="btn ghost" href="{CH}" rel="noopener">▶ Ir al canal</a></p></div></section>
<section><h2>Próximos estrenos</h2><ol class="cal" id="proximos" aria-live="polite"><li>Cargando calendario…</li></ol></section>
<section><h2>Todo el contenido</h2>{filt}<div class="grid" id="grid">{"".join(card(x) for x in V)}</div></section>
<section class="how"><h2>Cómo usar las descargas</h2><ol><li>Abrí el tutorial o molde y tocá <b>Descargar slides (PDF)</b>.</li><li>Para los moldes, imprimí en A4 al 100 % («tamaño real») y medí el cuadrado de control de 2 × 2 cm.</li><li>Seguí los pasos explicados en cada página junto al video.</li><li>¿Querés todo junto? Usá <b>Descargar todos</b> (ZIP) o mirá la <a href="base-de-datos/index.html">base de datos</a>.</li></ol></section>'''
open('index.html','w').write(page('index.html','Tutoriales de dibujo, moldes y arte experimental','Tutoriales de dibujo paso a paso, moldes de papel y la serie Historia del arte experimental, con slides en PDF para descargar.',home,{"@context":"https://schema.org","@type":"WebSite","name":"Arte experimental v5x","url":B}))
tl=f'<h1>Tutoriales de dibujo</h1><p>{len(tuts)} tutoriales con explicación paso a paso y slides en PDF.</p><p>{dlall.replace("descargas/","../descargas/")}</p><div class="grid">{"".join(card(x,"../") for x in tuts)}</div>'
open('tutoriales/index.html','w').write(page('tutoriales/index.html','Tutoriales de dibujo','Todos los tutoriales de dibujo con PDF descargable.',tl))
# ---------- moldes ----------
M={'casita':dict(t='Molde de casita de papel',medidas=[('Frente y fondo','6 cm'),('Costados','5 cm'),('Alto de pared','5 cm'),('Pico del techo','4 cm'),('Techo','5 cm de pendiente + 0,5 cm de alero'),('Piso','6 × 5 cm'),('Casita armada','6 × 5 cm de base, 9 cm de alto')]),
 'robot-bulon':dict(t='Molde de robot Bulón',medidas=[('Cabeza','cubo de 4 × 4 × 4 cm'),('Cuerpo','caja de 5 × 3 × 4,5 cm'),('Pestañas de pegado','0,8 cm'),('Robot armado','unos 12 cm de alto')])}
for slug,m in M.items():
    x=next(v for v in V if v['id']=='molde-'+slug);pg=pages(x['pdf'])
    instr=pg[-1]
    def sect(name):
        mm=re.search(name+r'\n(.*?)(\n\n[A-ZÁ][a-zá ]+\n|\Z)',instr,re.S);return mm[1] if mm else ''
    stp=re.findall(r'^\d+\.\s(.*?)(?=^\d+\.\s|\n\n|\Z)',sect('Paso a paso')+'\n\n',re.S|re.M)
    stp=[' '.join(s.split()) for s in stp]
    mats=[l.strip('• ').strip() for l in sect('Materiales').split('\n') if l.strip().startswith('•')]
    tips=[' '.join(l.split()).strip('• ') for l in re.split(r'\n(?=•)',sect('Consejos')) if l.strip()]
    pv=''.join(f'<figure><a href="../img/p/molde-{slug}-{i}.webp"><img src="../img/p/molde-{slug}-{i}.webp" alt="Vista previa de la hoja {i} del {m["t"].lower()}" loading="lazy" width="538" height="760"></a><figcaption>Hoja {i} de {len(pg)}</figcaption></figure>' for i in range(1,len(pg)+1))
    ills=[f'../img/p/molde-{slug}-{i}.webp' for i in range(1,len(pg)+1)]
    st=''.join(f'<li class="step"><div><h3>Paso {i}</h3><p>{e(s)}</p></div></li>' for i,s in enumerate(stp,1))
    rows=''.join(f'<tr><th scope="row">{a}</th><td>{b}</td></tr>' for a,b in m['medidas'])
    body=f'''<article class="post"><p class="crumbs"><a href="index.html">Moldes</a> › {m["t"]}</p>
<div class="post-head"><img class="cover" src="../{x["imagen"]}" alt="Hoja 1 del {m["t"].lower()}" width="538" height="760"><div><p class="kicker">Molde para imprimir {badge(x)}</p><h1>{m["t"]}</h1>
<p>Molde original en A4 ({len(pg)} hojas) con piezas para recortar, doblar y pegar, más la hoja de instrucciones. Video: próximamente.</p>
<p class="actions"><a class="btn" href="../{x["pdf"]}" download>⬇ Descargar molde (PDF)</a> {share(m["t"])}</p></div></div>
<div class="safety" role="note"><b>⚠ Seguridad:</b> si sos chico o chica, recortá con tijera de punta redonda y con un adulto cerca. Usá pegamento escolar no tóxico, poquito y en un lugar ventilado, y guardá la tijera cerrada al terminar.</div>
<h2>Vista previa del PDF</h2><div class="pv">{pv}</div>
<h2>Medidas</h2><table class="med"><caption>Medidas tomadas del molde (en cm)</caption><tbody>{rows}</tbody></table>
<h2>Materiales</h2><ul class="mat">{"".join(f"<li>{e(a)}</li>" for a in mats) or "<li>Hoja A4, tijera, pegamento y regla.</li>"}</ul>
<h2>Antes de recortar</h2><p>Imprimí en A4 al 100 % («tamaño real», sin «ajustar a la página») y medí el cuadrado de control: tiene que dar 2 × 2 cm.</p>
<h2>Paso a paso</h2><ol class="steps plain">{st or "<li>Seguí la hoja de instrucciones del PDF.</li>"}</ol>
<p class="lic">Las ilustraciones de los pasos están en la última hoja del PDF (vista previa arriba).</p>
<h2>Consejos</h2><ul class="tips">{"".join(f"<li>{e(t)}</li>" for t in tips)}</ul>
{gallery("molde-"+slug+"-video","../",title="Diapositivas del video (Google Slides)")}
<h2>Video</h2>{video_block(x)}
<nav class="pn"><a href="index.html">← Todos los moldes</a><a href="{"robot-bulon" if slug=="casita" else "casita"}.html">{"Molde de robot Bulón" if slug=="casita" else "Molde de casita de papel"} →</a></nav></article>'''
    ld={"@context":"https://schema.org","@type":"HowTo","name":m['t'],"image":B+x['imagen'],"supply":[{"@type":"HowToSupply","name":a} for a in mats],"step":[{"@type":"HowToStep","text":s} for s in stp]}
    open(x['pagina'],'w').write(page(x['pagina'],m['t'],f'{m["t"]} para imprimir en A4: medidas, paso a paso y PDF gratis.',body,ld,x['imagen']))
ml=f'<h1>Moldes de papel</h1><p>Imprimí, recortá y armá. Cada molde trae medidas, pasos y consejos.</p><div class="grid">{"".join(card(x,"../") for x in V if x["tipo"]=="molde")}</div>'
open('moldes/index.html','w').write(page('moldes/index.html','Moldes de papel','Moldes de papel para imprimir gratis en PDF.',ml))
# ---------- historia ----------
os.makedirs('historia',exist_ok=True)
eps=''.join(f'<article class="ep" id="ep{i}"><img src="../img/historia/ep{i:02d}.svg" alt="" width="320" height="180"><div><p class="kicker">Episodio {i} {badge(x)}</p><h2>{e(H[i-1][0])}</h2><p>{e(x["resumen"])}</p>{video_block(x) if x["estado"]=="programado" else "<p class=date>Pendiente de producción.</p>"}</div></article>' for i,x in enumerate([v for v in V if v['tipo']=='historia'],1))
hb=f'<h1>Historia del arte experimental</h1><p class="lead">Serie de 12 episodios planeados que recorre movimientos del arte del siglo XX hasta hoy. Los episodios 1 y 2 ya están hechos y programados; el resto está en producción.</p><p class="lic">Las ilustraciones de esta página son composiciones abstractas propias del sitio, no reproducciones de obras.</p><div class="eps">{eps}</div>'
open('historia/index.html','w').write(page('historia/index.html','Historia del arte experimental (serie)','Serie de 12 episodios sobre la historia del arte experimental: Dadaísmo, Surrealismo, Futurismo y más.',hb))
# ---------- base de datos ----------
os.makedirs('base-de-datos',exist_ok=True)
db='''<h1>Base de datos del canal</h1><p>Todos los videos, Shorts, moldes y episodios en una tabla. Fuente única: <a href="../data/videos.json">data/videos.json</a>. Sin métricas: solo estado y fechas.</p>
<div class="dbbar"><label>Buscar <input id="q" type="search" placeholder="gato, molde, dadaísmo…"></label>
<label>Tipo <select id="ft"><option value="">Todos</option><option>tutorial</option><option>short</option><option>molde</option><option>historia</option></select></label>
<label>Tema <select id="fm"><option value="">Todos</option><option>animal</option><option>insecto</option><option>molde</option><option>historia</option></select></label>
<label>Estado <select id="fe"><option value="">Todos</option><option>publicado</option><option>programado</option><option>pendiente</option></select></label></div>
<p id="cnt" aria-live="polite"></p><div class="tw"><table id="db"><thead><tr><th><button data-k="titulo">Título</button></th><th><button data-k="tipo">Tipo</button></th><th><button data-k="tema">Tema</button></th><th><button data-k="estado">Estado</button></th><th><button data-k="fecha">Fecha</button></th><th>Enlaces</th></tr></thead><tbody></tbody></table></div>'''
open('base-de-datos/index.html','w').write(page('base-de-datos/index.html','Base de datos del canal','Tabla interactiva con todos los videos, Shorts, moldes y episodios del canal Arte experimental v5x.',db))
# ---------- blog (posts/*.html: 1ª línea <!--{json}-->; ver posts/README.md) ----------
import glob
os.makedirs('blog',exist_ok=True);P=[]
for f in sorted(glob.glob('posts/[!_]*.html')):
    raw=open(f).read();m=re.match(r'<!--(\{.*?\})-->\n',raw,re.S);meta=json.loads(m[1]);meta['body']=raw[m.end():];P.append(meta)
P.sort(key=lambda x:x['fecha'],reverse=True)
def ytembed(m):return f'<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/{m[1]}" title="Video de YouTube" loading="lazy" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture; fullscreen" allowfullscreen></iframe></div>'
for x in P:
    body=slide_codes(re.sub(r'\{YT:([\w-]{11})\}',ytembed,x['body'].replace('{R}','../')),'../')
    ns=body.count('<section class="slide">');cnt=[0]
    def numslide(m):
        cnt[0]+=1;k=cnt[0]
        return f'<section class="slide" id="d{k}"><span class="brand">Arte experimental v5x · {k}/{ns}</span>'
    body=re.sub(r'<section class="slide">',numslide,body)
    body=body.replace('</section>','<p class="handle">@Arteexperimentalv5x</p></section>')
    cimg=x.get('portada')
    cover=f'<header class="deck-cover"><span class="brand">Arte experimental v5x</span><div><p class="sk">{e(x.get("serie","Blog") )} · {e((x.get("etiquetas") or ["post"])[0])}</p><h1>{e(x["titulo"])}</h1><p class="lead">{e(x["resumen"])}</p><hr class="rule"><p class="handle">{ns} diapositivas · {fmt(x["fecha"])}</p></div>'+(fig(*next(it for it in deck_of(cimg[0]) if it[0].endswith(f"-{cimg[1]}.webp")),'../') if cimg else '')+'</header>'
    body=cover+body
    ld={"@context":"https://schema.org","@type":"Article","headline":x['titulo'],"description":x['resumen'],"image":B+x['imagen'],"datePublished":x['fecha'],"dateModified":x['fecha'],"inLanguage":"es-AR","mainEntityOfPage":B+f"blog/{x['slug']}.html","author":{"@type":"Organization","name":"Arte experimental v5x","url":CH},"publisher":{"@type":"Organization","name":"Arte experimental v5x","url":B},"keywords":", ".join(x.get('etiquetas',[]))}
    open(f"blog/{x['slug']}.html",'w').write(page(f"blog/{x['slug']}.html",x['titulo'],x['resumen'],f'<article class="post deck"><p class="crumbs"><a href="index.html">Blog</a> › {e(x["titulo"])}</p>{body}<p class="kicker">Publicado: {fmt(x["fecha"])} · {e(", ".join(x.get("etiquetas",[])))}</p><p>{share(x["titulo"])}</p><p><a href="index.html">← Volver al blog</a></p></article>',ld,x['imagen']))
docs=sorted(glob.glob('docs/*.pdf'))
dl=''.join(f'<li><a href="../{d}" download>{e(os.path.basename(d))}</a> ({os.path.getsize(d)//1024} KB)</li>' for d in docs)
bl='<h1>Blog</h1><p class="lead">Guías útiles para dibujar, armar moldes y conocer el arte experimental.</p><div class="grid">'+''.join(f'<article class="card"><a href="{x["slug"]}.html"><img src="../{x["imagen"]}" alt="" loading="lazy" width="480" height="300"></a><div class="cb"><span class="tag">post</span><h3><a href="{x["slug"]}.html">{e(x["titulo"])}</a></h3><p class="date">{fmt(x["fecha"])}</p><p>{e(x["resumen"])}</p></div></article>' for x in P)+'</div>'
if dl: bl+=f'<h2>Documentos</h2><ul>{dl}</ul>'
open('blog/index.html','w').write(page('blog/index.html','Blog','Guías y posts útiles del canal Arte experimental v5x: dibujo, moldes de papel e historia del arte.',bl,{"@context":"https://schema.org","@type":"Blog","name":"Blog de Arte experimental v5x","url":B+"blog/","blogPost":[{"@type":"BlogPosting","headline":x['titulo'],"url":B+f"blog/{x['slug']}.html","datePublished":x['fecha']} for x in P]}))
# ---------- sitemap ----------
urls=['','tutoriales/','moldes/','historia/','base-de-datos/','blog/']+[f"blog/{x['slug']}.html" for x in P]+[x['pagina'] for x in V if not x['pagina'].startswith('historia')]
open('sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{B}{u}</loc><lastmod>2026-10-26</lastmod></url>\n' for u in urls)+'</urlset>\n')
print('ok',len(V))
