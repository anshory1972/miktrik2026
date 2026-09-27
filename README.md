# Mikroekonometrika 2026

Course site for microeconometrics: slides, do-files, and data for students to
download.

Static HTML served by GitHub Pages. No build step, no framework, no server.

---

## Published

The repository is `anshory1972/miktrik2026` and the site is live at

**https://anshory1972.github.io/miktrik2026/**

Pages deploys from `main` at the repository root. Every `git push` to `main`
republishes within a minute or so.

The `.nojekyll` file is required. Without it GitHub runs Jekyll, which ignores
files and folders beginning with an underscore, including `_template.html`.

---

## Repository layout

```
index.html                     course home, list of materials
topics/                        one page per topic
  _template.html               copy this to start a new topic
  01-lpm-logit-probit.html
assets/
  style.css                    house style, shared by every page
materials/
  slides/                      lecture PDFs
  stata/                       do-files
  data/                        datasets
```

### Adding a topic

1. Copy `topics/_template.html` to `topics/NN-slug.html`.
2. Fill in the title, the prose, and the download rows.
3. Put the files in `materials/`.
4. Add a card for it in `index.html`.
5. Commit and push.

---

## Limits to respect

| Limit | Value |
|---|---|
| Published GitHub Pages site, total | 1 GB |
| Single file GitHub will accept | 100 MB |

Current `materials/` is about 10 MB. If a dataset ever approaches the file cap,
link to it rather than committing it.

---

## Verifying a change

Layout faults in these pages are almost always horizontal overflow or a CSS
specificity clash. Both are cheap to test. Render each page in headless Chrome
inside an iframe of an exact phone width and assert `scrollWidth == clientWidth`,
then look at the screenshot. Headless Chrome will not lay out below about 485px,
so the iframe is the only honest way to measure 360 and 390.

One trap already bit this stylesheet and is documented in `assets/style.css`:
`.prose a` is specificity (0,1,1) and beats a bare `.btn` at (0,1,0), which
painted a button label terracotta on a terracotta ground. Button rules repeat
the `a` element for that reason.

---

## Note on the removed discussion forum

An earlier version of this site embedded a Telegram-backed public forum. It did
work, but the setup proved too fragile to be worth keeping. A thread is
addressed by its channel post number, so deleting a post destroys that thread
and all its comments permanently, and two undocumented Telegram rules had to be
found by trial.

Removed on 2026-09-27 at the author's request. The full implementation and its
documentation remain in git history at commit `5b3a890` if it is ever wanted
again.
