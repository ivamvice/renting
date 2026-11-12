"""Genera index.html estático a partir del HTML del artifact. Uso: python3 build_index.py <artifact.html>"""
import sys, re, pathlib
s = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
a = s.index("  (async()=>{"); b = s.rindex("})();")
loader = '''  fetch("data.json",{cache:"no-store"}).then(r=>r.json()).then(d=>{
    state.img=d.imagenes||{}; showMeta(d.meta||null);
    renderFin((d.financiacion||[]).filter(r=>r&&typeof r.cuota==="number"));
    state.rows=(d.ofertas||[]).filter(r=>r&&typeof r.cuota==="number").map(r=>(r.entrada=+r.entrada||0,r));
    buildFilters(); render();
  }).catch(()=>{$("#rows").innerHTML='<tr><td colspan="10" class="empty">No se han podido cargar las ofertas.</td></tr>';});
'''
s = s[:a] + loader + s[b:]
s = re.sub(r'<meta name="claude:[^>]*>\s*', '', s)
s = s.replace("Cargando las ofertas guardadas. Si no aparecen, inicia sesión en claude.ai para ver la tabla.", "Cargando ofertas…")
assert "claude.use" not in s
if not s.lstrip().lower().startswith("<!doctype"):
    i = s.index("</style>") + len("</style>")
    head = '<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n<meta name="description" content="Cuotas de renting para particulares en España por marca y modelo, con o sin entrada, IVA incluido, duración del contrato y km/año.">\n'
    s = "<!doctype html>\n<html lang=\"es\">\n<head>\n" + head + s[:i] + "\n</head>\n<body>\n" + s[i:] + "\n</body>\n</html>\n"
pathlib.Path(__file__).with_name("index.html").write_text(s, encoding="utf-8"); print("index.html", len(s))
