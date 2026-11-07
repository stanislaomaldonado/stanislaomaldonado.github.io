# Stanislao Maldonado — personal website

English-language academic website prepared for GitHub Pages.

## Site structure

- `index.html`: biography, recent research, news, selected publications and engagement.
- `publications/index.html`: journal articles, book chapters and books.
- `research/index.html`: working papers and ongoing studies, with search and topic filters.
- `teaching/index.html`: teaching history by institution.
- `projects/index.html`: online course, workshop and teaching assistant.
- `assets/`: styles, research filtering script, photographs and institutional logo.

This is a static HTML/CSS/JavaScript site. It requires no package installation or build step.

## Publishing

Configure **Settings → Pages → Deploy from a branch → main → /(root)**.
The `.nojekyll` file serves the site directly as static files.

The existing domain is `www.stanislaomaldonado.org`. Canonical URLs and the sitemap
retain that domain during the transition. The repository intentionally contains no
`CNAME` file: configure the custom domain only when its DNS transition is ready.

## Local preview

Run `python -m http.server 4173` in this folder and open `http://127.0.0.1:4173/`.

## Maintenance

Edit the relevant HTML files to update content. Shared styles live in `assets/home.css`
and `assets/sections.css`; the research search/filter logic is in `assets/research.js`.
The header and footer are repeated in the five pages and should be kept consistent.
News uses dates only where a source provides one; the date on the price-controls
item identifies the paper version. Teaching dates and external PDF/CV links were
migrated from the original site and can be updated independently.

The photographs were supplied by the site owner. Their original files are not
included; this repository contains web-optimized copies and the institutional logo.
