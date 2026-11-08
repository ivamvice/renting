"""Genera data.json para la web a partir de una exportación de la base de datos del artifact.

Uso: python3 build_data.py <carpeta_exportada>
La carpeta contiene ofertas/*.json, imagenes/*.json y meta/estado.json
(ArtifactData list con out_dir). Escribe data.json junto a este script.
"""
import json, sys, pathlib
src = pathlib.Path(sys.argv[1])
out = pathlib.Path(__file__).with_name("data.json")
load = lambda p: json.loads(p.read_text(encoding="utf-8"))
ofertas = sorted((load(p) for p in (src / "ofertas").glob("*.json")), key=lambda d: (d["cuota"], d["marca"], d["modelo"]))
imagenes = {p.stem: load(p) for p in sorted((src / "imagenes").glob("*.json"))}
meta = load(src / "meta" / "estado.json")
out.write_text(json.dumps({"meta": meta, "ofertas": ofertas, "imagenes": imagenes}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(f"data.json: {len(ofertas)} ofertas, {len(imagenes)} imágenes, {out.stat().st_size//1024} KB")
