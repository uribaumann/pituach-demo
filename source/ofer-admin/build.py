"""Builds admin.html (local) and artifact.html (publishable) from src/admin.src.html, inlining the shared app assets."""
import base64, json, pathlib, re, sys
root = pathlib.Path(__file__).parent
mime = {".jpg": "image/jpeg", ".png": "image/png", ".svg": "image/svg+xml", ".pdf": "application/pdf"}
assets = {p.stem: [mime[p.suffix], base64.b64encode(p.read_bytes()).decode()]
          for p in sorted((root / "assets").iterdir()) if p.suffix in mime}
src = (root / "src" / "admin.src.html").read_text(encoding="utf-8")
boot = ("const A0=" + json.dumps(assets) + ";const A={},AB={};for(const k in A0){const b=atob(A0[k][1]),u=new Uint8Array(b.length);"
        "for(let i=0;i<b.length;i++)u[i]=b.charCodeAt(i);AB[k]=new Blob([u],{type:A0[k][0]});A[k]=URL.createObjectURL(AB[k])}")
assert "/*__ASSETS__*/" in src
# Real names only with --names (private claude.ai build); the public site gets job titles only.
pf = root / ("people.private.json" if "--names" in sys.argv and (root / "people.private.json").exists() else "people.public.json")
assert "/*__PEOPLE__*/[]" in src
src = src.replace("/*__PEOPLE__*/[]", pf.read_text(encoding="utf-8").strip())
cf = root / ("config.private.json" if "private" in pf.name else "config.public.json")
assert "/*__CFG__*/{}" in src
src = src.replace("/*__CFG__*/{}", cf.read_text(encoding="utf-8").strip())
# Public build: if a team code is set (file team.code, never committed), real names and emails go in encrypted.
vault = "null"
code_file = root / "team.code"
if "private" not in pf.name and code_file.exists() and (root / "people.private.json").exists():
    import os
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    salt, iv, n = os.urandom(16), os.urandom(12), 600000
    key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=n).derive(code_file.read_text(encoding="utf-8").strip().encode())
    data = json.dumps({"people": json.loads((root / "people.private.json").read_text(encoding="utf-8")),
                       "cfg": json.loads((root / "config.private.json").read_text(encoding="utf-8"))}, ensure_ascii=False).encode()
    b64 = lambda x: base64.b64encode(x).decode()
    vault = json.dumps({"s": b64(salt), "iv": b64(iv), "n": n, "c": b64(AESGCM(key).encrypt(iv, data, None))})
assert "/*__VAULT__*/null" in src
src = src.replace("/*__VAULT__*/null", vault)
out = src.replace("/*__ASSETS__*/", boot)
(root / "admin.html").write_text(out, encoding="utf-8")
art = re.sub(r'<!doctype html>|</?html[^>]*>|</?head>|</?body[^>]*>|<meta charset[^>]*>|<meta name="viewport"[^>]*>', "", out)
(root / "artifact.html").write_text(art, encoding="utf-8")
print("built", (root / "admin.html").stat().st_size // 1024, "KB", "with names" if "private" in pf.name else ("roles only + encrypted names" if vault != "null" else "roles only"))
