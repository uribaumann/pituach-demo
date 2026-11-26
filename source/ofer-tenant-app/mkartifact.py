"""Turns the built index.html into the claude.ai page (artifact.html)."""
import re, pathlib
root = pathlib.Path(__file__).parent
s = (root / "index.html").read_text(encoding="utf-8")
s = re.sub(r'<!doctype html>|<!DOCTYPE html>', '', s)
s = re.sub(r'</?html[^>]*>|</?head>|</?body[^>]*>|<meta[^>]*>', '', s)
s = re.sub(r'<title>.*?</title>', '<title>Pituach Residents App</title>', s, flags=re.S)
s = s.replace('.phone{width:100%;height:100dvh', '.phone{width:100%;height:100%')
s = s.replace('height:100vh;height:100dvh;max-height:none;border-radius:0', 'height:100%;max-height:none;border-radius:0')
s = s.replace('padding-top:max(14px,env(safe-area-inset-top))', 'padding-top:14px')
(root / "artifact.html").write_text(s, encoding="utf-8")
print("artifact.html", len(s) // 1024, "KB")
