#!/usr/bin/env python3
"""Borra metadata (EXIF/XMP/autor) de PDFs e imágenes. Uso: python3 tools/limpiar.py archivo_o_carpeta ..."""
import sys,os,pathlib
def pdf(p):
    import pikepdf
    with pikepdf.open(p,allow_overwriting_input=True) as d:
        if '/Info' in d.trailer: del d.trailer['/Info']
        if '/Metadata' in d.Root: del d.Root['/Metadata']
        d.save(p)
def img(p):
    from PIL import Image
    im=Image.open(p);fmt=im.format
    clean=Image.new(im.mode,im.size);clean.putdata(list(getattr(im,"get_flattened_data",im.getdata)()))
    if im.mode=='P':clean.putpalette(im.getpalette())
    clean.save(p,fmt,**({'quality':90} if fmt in('JPEG','WEBP') else {}))
for a in sys.argv[1:] or ['docs','img/subidas']:
    for p in ([pathlib.Path(a)] if os.path.isfile(a) else pathlib.Path(a).rglob('*')):
        s=p.suffix.lower()
        if s=='.pdf':pdf(p);print('limpio',p)
        elif s in('.jpg','.jpeg','.png','.webp'):img(p);print('limpio',p)
