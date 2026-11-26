"""Builds index.html: inlines everything in assets/ into src/index.src.html as data URIs."""
import base64, json, pathlib
root = pathlib.Path(__file__).parent
mime = {".jpg": "image/jpeg", ".png": "image/png", ".svg": "image/svg+xml", ".pdf": "application/pdf"}
assets = {p.stem: f"data:{mime[p.suffix]};base64,{base64.b64encode(p.read_bytes()).decode()}"
          for p in sorted((root / "assets").iterdir()) if p.suffix in mime}
src = (root / "src" / "index.src.html").read_text(encoding="utf-8")
assert "/*__ASSETS__*/" in src
en = (root / "src" / "en.json")
src = src.replace("/*__EN__*/{}", en.read_text(encoding="utf-8") if en.exists() else "{}")
(root / "index.html").write_text(src.replace("/*__ASSETS__*/", "const A0=" + json.dumps(assets) + ";const A={};for(const k in A0){try{const m=A0[k].match(/^data:(.*?);base64,(.*)$/),b=atob(m[2]),u=new Uint8Array(b.length);for(let i=0;i<b.length;i++)u[i]=b.charCodeAt(i);A[k]=URL.createObjectURL(new Blob([u],{type:m[1]}))}catch(e){A[k]=A0[k]}}"), encoding="utf-8")
print("built index.html", (root / "index.html").stat().st_size // 1024, "KB")
