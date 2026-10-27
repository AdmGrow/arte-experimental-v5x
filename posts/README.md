# Cómo agregar contenido al blog

## Post nuevo
1. Copiá `posts/_plantilla.html` a `posts/AAAA-MM-DD-slug.html` (los archivos que empiezan con `_` no se publican).
2. Editá la primera línea (JSON): `titulo`, `slug` (sin espacios ni tildes), `fecha` (AAAA-MM-DD), `resumen`, `imagen`, `etiquetas`.
3. Escribí el cuerpo en HTML simple (`<p>`, `<h2>`, `<ul>`, `<figure>`).
   - `{R}` = raíz del sitio (ej. `{R}moldes/index.html`).
   - `{YT:ID}` inserta un video de YouTube (ID de 11 caracteres de `youtu.be/ID`).
4. Corré `python3 tools/build.py`: genera `blog/<slug>.html`, el índice, JSON-LD Article y el sitemap.

## Documentos (PDF) e imágenes
- PDFs → `docs/`  ·  imágenes (jpg/png/webp/svg) → `img/subidas/`.
- Antes de commitear: `tools/limpiar.sh` (borra EXIF/XMP/autor). Verificá con `pdfinfo docs/x.pdf` que no haya Author.
- Los PDFs de `docs/` aparecen solos en la sección «Documentos» de `/blog/`.
- Nunca pongas mails personales; commits sólo con el noreply de GitHub.
