# tobinhanspal.github.io

Academic homepage for Tobin Hanspal. Plain static HTML, CSS, and one small JS
file. No build system is required to serve it, and GitHub Pages publishes the
repository root as-is (`.nojekyll` disables Jekyll processing).

## Layout

```
index.html            Research page (current research, publications, resting papers)
robots.txt            Crawler policy, see "Keeping the site out of search results"
survey.html           Appendix materials for the REStat COVID-19 paper
assets/css/style.css  All styling
assets/img/photo.jpg  Portrait (see "Adding the portrait" below)
files/cv.pdf          CV
files/oappendix.pdf   Online appendix
files/survey_instructions.pdf
build/                Optional generator, see "Editing content"
```

## Abstracts

Each abstract is a native HTML `<details>` element, so clicking "Abstract"
unrolls it. The site ships no JavaScript at all: the disclosure behaviour is
the browser's own, which means it works with scripting disabled, is keyboard
accessible, and prints correctly.

## Editing content

Two options, pick either.

**Edit the HTML directly.** `index.html` is readable static markup. A paper is
one `<article class="paper">` block. Copy an existing one and change the text.

**Or regenerate.** Content lives in `build/papers.py` and abstract text in
`build/abstracts.json`, keyed by the `key` field of each paper. Then run:

```
python build/build.py
```

This rewrites `index.html` and `survey.html`. A paper with no matching key in
`abstracts.json` simply renders without an Abstract toggle.

## Abstracts still to add

Three papers have no abstract on file, so they currently render
without a toggle. To add one, put the text in `build/abstracts.json` under the
listed key and set that key on the paper in `build/papers.py`, then rebuild.

| Paper | Suggested key |
| --- | --- |
| Do Financial Misconduct Experiences Spur White-Collar Crime? | `misconduct` |
| Political Corruption, Trust, and Household Stock Market Participation | `corruption` |
| Does Financial Technology Affect Household Savings Behavior? | `fintech-savings` |

## Portrait

`assets/img/photo.jpg` is the full frame from the 2018 shoot, resized to 540px
wide and saved as an optimised JPEG (21 KB, down from a 1.3 MB PNG source).

`assets/img/photo-portrait.jpg` is an alternative crop that trims the empty
left third so the face fills more of the sidebar. To use it instead, change
the `src` on the `.portrait` image in `build/build.py` (the `SIDEBAR` block)
and rerun `python build/build.py`, or edit the two HTML files directly.

Source file: `Dropbox/Personal/ProPhoto_2018/PicturePeopleMyZeil-3_retouch.png`

## Keeping the site out of search results

Both pages carry `<meta name="robots" content="noindex, nofollow">`, emitted
from the `NOINDEX` flag at the top of `build/build.py`. The site is publicly
reachable, it just should not turn up in search results.

`robots.txt` deliberately *allows* crawling. A crawler has to fetch a page to
see its `noindex`, so blocking with `Disallow: /` would hide the instruction
and could leave a bare URL indexed anyway.

To go live in search results:

1. Set `NOINDEX = False` in `build/build.py`
2. Run `python build/build.py`
3. Delete `robots.txt`
4. Commit and push

## Local preview

```
python -m http.server 8000
```

Then open http://localhost:8000.

## Custom domain

`www.tobinhanspal.com` is not configured yet. To switch it on, add a file named
`CNAME` at the repository root containing `www.tobinhanspal.com`, then create a
DNS `CNAME` record pointing `www` at `tobinhanspal.github.io`. Do this after
confirming the site works at the `github.io` address, since an unconfigured
custom domain makes the site unreachable.
