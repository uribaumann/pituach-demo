"""Builds the residents app from src/index.src.html.

index.html      everything inlined as data URIs (used for the claude.ai page via mkartifact.py)
index.web.html  with --web: photos and PDFs stay separate files under assets/, so phones parse a small page fast
The splash images are always inlined, pre-whitened, so the opening screen paints at once.
"""
import base64, io, json, pathlib, re, sys
from PIL import Image

root = pathlib.Path(__file__).parent
mime = {".jpg": "image/jpeg", ".png": "image/png", ".svg": "image/svg+xml", ".pdf": "application/pdf"}
files = sorted(p for p in (root / "assets").iterdir() if p.suffix in mime)
web = "--web" in sys.argv

def data_uri(p):
    return f"data:{mime[p.suffix]};base64,{base64.b64encode(p.read_bytes()).decode()}"

def white_png(p):
    im = Image.open(p).convert("RGBA")
    alpha = im.getchannel("A")
    out = Image.new("RGBA", im.size, (255, 255, 255, 0))
    out.putalpha(alpha)
    buf = io.BytesIO()
    out.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

src = (root / "src" / "index.src.html").read_text(encoding="utf-8")
assert "/*__ASSETS__*/" in src
en = root / "src" / "en.json"
src = src.replace("/*__EN__*/{}", en.read_text(encoding="utf-8") if en.exists() else "{}")

# Splash: inline white images directly in the markup (no filter, no wait for scripts).
for key in ("bird", "wordmark", "embrace"):
    tag = f'data-a="{key}"'
    assert tag in src, key
    src = src.replace(f'<img class="{ {"bird": "bd", "wordmark": "wm", "embrace": "em"}[key] }" {tag}',
                      f'<img class="{ {"bird": "bd", "wordmark": "wm", "embrace": "em"}[key] }" src="{white_png(root / "assets" / (key + ".png"))}"', 1)
src = src.replace('<img class="of" data-a="ofer"', f'<img class="of" src="{data_uri(root / "assets" / "ofer.svg")}"', 1)

if web:
    assets = {p.stem: f"assets/{p.name}" for p in files}
    boot = "const A0=" + json.dumps(assets) + ";const A=A0;"
    out = root / "index.web.html"
else:
    assets = {p.stem: data_uri(p) for p in files}
    boot = ("const A0=" + json.dumps(assets) + ";const A={};for(const k in A0){try{const m=A0[k].match(/^data:(.*?);base64,(.*)$/),"
            "b=atob(m[2]),u=new Uint8Array(b.length);for(let i=0;i<b.length;i++)u[i]=b.charCodeAt(i);"
            "A[k]=URL.createObjectURL(new Blob([u],{type:m[1]}))}catch(e){A[k]=A0[k]}}")
    out = root / "index.html"
out.write_text(src.replace("/*__ASSETS__*/", boot), encoding="utf-8")
print("built", out.name, out.stat().st_size // 1024, "KB")
