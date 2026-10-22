# Zhixin Wang, PhD

Personal website, hosted on GitHub Pages. Plain HTML and CSS, no build step.

## Pages

- `index.html`: Home (intro, highlights, links to every page)
- `career.html`: Experience, education, skills, languages
- `research.html`: Research focus, publications, honors, certifications
- `cooking.html`: Cooking and baking
- `pets.html`: Pets
- `styles.css`: Shared styling, with automatic light and dark themes
- `bunny.svg`: The bunny mascot used in the header, home page, and footer

Each page repeats the same header and footer, so a new page or nav link needs adding to every file.

## Languages

The English pages in the root are the source. French, Spanish and Chinese copies live in `fr/`, `es/` and `zh/` and are generated, so don't edit them by hand. After changing an English page:

1. Add any new or changed text, with its translations, to `i18n/translations.py`.
2. Run `python3 i18n/build.py` from the repo root. It refreshes the language switcher and rewrites the translated pages, and warns about any text it couldn't translate.

## Photos

Put images in a `photos/` folder and swap a placeholder such as `<div class="photo">…</div>` for `<div class="photo"><img src="photos/cat.jpg" alt="…"></div>`. The home page portrait works the same way with `<div class="portrait">`.

## Publishing

In the repository's **Settings → Pages**, set **Source** to "Deploy from a branch", branch `main`, folder `/ (root)`.

The site uses the custom domain **itszhixinwang.com** (see `CNAME`). Its DNS is managed in Cloudflare and must point at GitHub Pages with "DNS only" records.
