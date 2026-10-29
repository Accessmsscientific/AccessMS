# Access MS Scientific — accessms.ca

The live website is everything in **`site/`** (plain HTML/CSS, no build step).
Pushing to `main` deploys `site/` to GitHub Pages via `.github/workflows/static.yml`.

- Edit text directly in `site/*.html`; styles are in `site/assets/css/style.css`.
- `tools/build_site.py` regenerates all pages from one script (`python tools/build_site.py site`) —
  handy for site-wide changes such as the navigation or footer. Note it overwrites the HTML files.
- `_legacy/` holds the previous (2023) site for reference; it is not published.
