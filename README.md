# Stanislao Maldonado — personal website

English-language academic website prepared for GitHub Pages.

## Site structure

- `index.html`: biography, recent research, news, selected publications and engagement.
- `publications/index.html`: journal articles, book chapters and books.
- `research/index.html`: working papers and ongoing studies, with search and topic filters.
- `teaching/index.html`: teaching history by institution.
- `projects/index.html`: online course, workshop and teaching assistant.
- `assets/`: styles, research filtering script, photographs and institutional logo.
- `documents/`: the PDFs served directly by this site, grouped by subject.
- `content/documents.json`: stable document IDs, file paths, versions, sizes and SHA-256 checksums.
- `scripts/`: maintenance and validation helpers; these do not run in the visitor's browser.

This is a static HTML/CSS/JavaScript site. It requires no package installation or build step.

## Publishing

Configure **Settings → Pages → Deploy from a branch → main → /(root)**.
The `.nojekyll` file serves the site directly as static files.

The custom domain is `www.stanislaomaldonado.org`. Keep the tracked `CNAME` file
and the canonical URLs when making updates. The four apex A records and the `www`
CNAME are configured at the domain provider. GitHub Pages manages the TLS certificate.

## Local preview

Run `python -m http.server 4173` in this folder and open `http://127.0.0.1:4173/`.

## Maintenance

This repository is the authoritative website source. Earlier one-off design builders
and content inventories in the working workspace are historical inputs and must not
be run over this checkout.

Edit the relevant HTML files to update content. Shared styles live in `assets/home.css`
and `assets/sections.css`; the research search/filter logic is in `assets/research.js`.
The header and footer are repeated in the five pages and should be kept consistent.
News uses dates only where a source provides one; the date on the price-controls
item identifies the paper version. Teaching dates were migrated from the original site.

## Documents and stable URLs

All PDFs previously linked directly from Dropbox, together with the existing Springer
appendix and RIDGE program, are now served from `documents/`. The original PDF bytes
are preserved. Journal, DOI, registry, course and institutional links remain external
references. The IDB working paper is also hosted locally, with its published title, version and attribution. Publisher links remain available as references.

The `path` of a document is its stable public address. For example,
`documents/research/price-controls-motivated-beliefs.pdf` is shared by the homepage,
News and Research. Every HTML link to a registered PDF carries `data-document-id`
so that a future maintenance skill can find its uses reliably.

To replace a registered PDF, keep its ID and path. With Python and `pypdf` installed:

```powershell
python scripts/update_document.py --id R02 --source "C:/path/new-paper.pdf" --version 2026-12-01
python scripts/validate_site.py
```

The update helper checks the PDF, replaces the file at the existing address and updates
its version, page count, size and checksum in the catalog. It does not invent new dates
or alter the page's editorial content. Update visible paper dates and coauthor details
when a new version requires them, then preview the page before committing and pushing.

To add a document, use a descriptive lowercase filename under the appropriate
`documents/` subdirectory, create a unique entry in `content/documents.json`, and add
relative links with its `data-document-id`. Then run the validator. The validator
checks local files, HTML anchors, PDF references, registry checksums and the custom domain.

The photographs were supplied by the site owner. Their original files are not
included; this repository contains web-optimized copies and the institutional logo.
