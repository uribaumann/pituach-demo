"""Builds admin.html (local) and artifact.html (publishable) from src/admin.src.html, inlining the shared app assets."""
import base64, json, pathlib, re
root = pathlib.Path(__file__).parent
mime = {".jpg": "image/jpeg", ".png": "image/png", ".svg": "image/svg+xml", ".pdf": "application/pdf"}
assets = {p.stem: [mime[p.suffix], base64.b64encode(p.read_bytes()).decode()]
          for p in sorted((root / "assets").iterdir()) if p.suffix in mime}
src = (root / "src" / "admin.src.html").read_text(encoding="utf-8")
boot = ("const A0=" + json.dumps(assets) + ";const A={},AB={};for(const k in A0){const b=atob(A0[k][1]),u=new Uint8Array(b.length);"
        "for(let i=0;i<b.length;i++)u[i]=b.charCodeAt(i);AB[k]=new Blob([u],{type:A0[k][0]});A[k]=URL.createObjectURL(AB[k])}")
assert "/*__ASSETS__*/" in src
out = src.replace("/*__ASSETS__*/", boot)
(root / "admin.html").write_text(out, encoding="utf-8")
art = re.sub(r'<!doctype html>|</?html[^>]*>|</?head>|</?body[^>]*>|<meta charset[^>]*>|<meta name="viewport"[^>]*>', "", out)
(root / "artifact.html").write_text(art, encoding="utf-8")
print("built", (root / "admin.html").stat().st_size // 1024, "KB")
