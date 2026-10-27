#!/usr/bin/env bash
# Borra metadata EXIF/XMP/autor de PDFs e imágenes antes de publicar.
# Uso: tools/limpiar.sh [archivos o carpetas]   (por defecto: docs/ img/subidas/)
set -e
cd "$(dirname "$0")/.."
T=("$@"); [ ${#T[@]} -eq 0 ] && T=(docs img/subidas)
if command -v exiftool >/dev/null; then
  exiftool -all= -overwrite_original -r -ext pdf -ext jpg -ext jpeg -ext png -ext webp "${T[@]}"
  command -v qpdf >/dev/null && find "${T[@]}" -iname '*.pdf' -exec qpdf --linearize --replace-input {} \;
else
  # Alternativa: python con pikepdf + pillow  (python3 -m venv v && v/bin/pip install pikepdf pillow; PY=v/bin/python)
  "${PY:-python3}" tools/limpiar.py "${T[@]}"
fi
# Control: no debe quedar Author/Creator en PDFs
for f in $(find "${T[@]}" -iname '*.pdf'); do pdfinfo "$f" 2>/dev/null | grep -iE '^(Author|Creator|Producer):' && echo "OJO: $f todavía tiene metadata"; done
echo "Listo."
