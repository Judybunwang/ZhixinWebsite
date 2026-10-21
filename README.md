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

## Photos

Put images in a `photos/` folder and swap a placeholder such as `<div class="photo">…</div>` for `<div class="photo"><img src="photos/cat.jpg" alt="…"></div>`. The home page portrait works the same way with `<div class="portrait">`.

## Publishing

In the repository's **Settings → Pages**, set **Source** to "Deploy from a branch", branch `main`, folder `/ (root)`.
