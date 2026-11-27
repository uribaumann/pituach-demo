#!/bin/bash
# Rebuilds the residents app and the admin center from source/, copies them into the site, commits and pushes.
# GitHub Pages republishes the site automatically after every push to main.
set -e
cd "$(dirname "$0")"
python3 source/ofer-tenant-app/build.py --web >/dev/null
python3 source/ofer-admin/build.py >/dev/null
noindex='<meta name="robots" content="noindex,nofollow">'
pwa='<link rel="manifest" href="manifest.webmanifest"><link rel="apple-touch-icon" href="apple-touch-icon.png"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-status-bar-style" content="default"><meta name="apple-mobile-web-app-title" content="Pituach">'
sed "s#<head>#<head>$noindex$pwa#" source/ofer-tenant-app/index.web.html > app/index.html
mkdir -p app/assets && cp source/ofer-tenant-app/assets/* app/assets/
cp source/ofer-tenant-app/pwa/* app/
apwa='<link rel="manifest" href="manifest.webmanifest"><link rel="apple-touch-icon" href="apple-touch-icon.png"><meta name="theme-color" content="#24344D"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-title" content="Pituach ניהול"><script src="reg.js" defer></script>'
sed "s|<head>|<head>$noindex$apwa|" source/ofer-admin/admin.html > admin/index.html
cp source/ofer-admin/pwa/* admin/
git add -A
git diff --cached --quiet && { echo "nothing changed"; exit 0; }
git commit -qm "${1:-Update demo}"
git -c push.negotiate=true push -q -u origin main && echo "pushed"
