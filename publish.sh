#!/bin/bash
# Rebuilds the residents app and the admin center from source/, copies them into the site, commits and pushes.
# GitHub Pages republishes the site automatically after every push to main.
set -e
cd "$(dirname "$0")"
python3 source/ofer-tenant-app/build.py >/dev/null
python3 source/ofer-admin/build.py >/dev/null
noindex='<meta name="robots" content="noindex,nofollow">'
sed "s#<head>#<head>$noindex#" source/ofer-tenant-app/index.html > app/index.html
sed "s#<head>#<head>$noindex#" source/ofer-admin/admin.html > admin/index.html
git add -A
git diff --cached --quiet && { echo "nothing changed"; exit 0; }
git commit -qm "${1:-Update demo}"
git -c push.negotiate=true push -q -u origin main && echo "pushed"
