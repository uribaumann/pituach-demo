# Pituach by the Sea · residents app demo

Clickable prototype of the residents app and its desktop admin center. All data is sample data.

- `index.html`: landing page with links to both parts
- `app/`: the residents app (open on a phone)
- `admin/`: the admin center (open on a computer)
- `source/`: the source both parts are built from

## Updating the site

```bash
./publish.sh "What changed"
```

The script rebuilds both parts, commits and pushes. GitHub Pages republishes within about a minute.

## Note

This is a demo. The admin login is checked in the browser only, and uploaded files stay in the browser that uploaded them. Do not upload real resident documents.
