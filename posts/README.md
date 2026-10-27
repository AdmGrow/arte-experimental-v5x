# Cómo agregar contenido al blog

## Post nuevo
1. Copiá `posts/_plantilla.html` (plantilla de **post semanal** con maqueta de diapositivas) a `posts/AAAA-MM-DD-slug.html` (los archivos que empiezan con `_` no se publican).
2. Editá la primera línea (JSON): `titulo`, `slug`, `fecha` (AAAA-MM-DD), `serie` (ej. «Post semanal #5»), `resumen`, `imagen` (captura real para el índice/og), `portada` (`["mazo", página]`, opcional), `etiquetas`.
3. Cuerpo = varias `<section class="slide">` (se numeran solas). Dentro: `<p class="sk">` (antetítulo celeste), `<h2>`, `<div class="split">` (texto + captura), `<div class="box">` (recuadro crema), `<p class="note">`, `<ul class="dots">`, `<table class="tbl">`.
   - `{SLIDE:mazo:página}` = captura real de una diapositiva con pie automático; `{GAL:mazo}` o `{GAL:mazo:2,3}` = galería. Nunca imágenes generadas por IA; si no hay captura útil, sin imagen.
   - `{R}` = raíz del sitio (ej. `{R}moldes/index.html`).
   - `{YT:ID}` inserta un video de YouTube (ID de 11 caracteres de `youtu.be/ID`).
4. Corré `python3 tools/build.py`: genera `blog/<slug>.html`, el índice, JSON-LD Article y el sitemap.

## Documentos (PDF) e imágenes
- PDFs → `docs/`  ·  imágenes (jpg/png/webp/svg) → `img/subidas/`.
- Antes de commitear: `tools/limpiar.sh` (borra EXIF/XMP/autor). Verificá con `pdfinfo docs/x.pdf` que no haya Author.
- Los PDFs de `docs/` aparecen solos en la sección «Documentos» de `/blog/`.
- Nunca pongas mails personales; commits sólo con el noreply de GitHub.

## Capturas de los videos de moldes
`data/slides-moldes.json` + `img/slides/` = slides de los videos de moldes renderizadas con `pdftoppm` a WebP (se omiten las que tienen la ilustración digital del modelo armado).
