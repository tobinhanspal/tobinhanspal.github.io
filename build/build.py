# -*- coding: utf-8 -*-
"""Generate index.html and survey.html.

Usage:  python build/build.py
"""
import json
import os
import sys
import html as H

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "build"))
from papers import WORKING, PUBLICATIONS, RESTING  # noqa: E402

ABS = json.load(open(os.path.join(ROOT, "build", "abstracts.json"), encoding="utf-8"))
e = H.escape


def authors_html(auth):
    if not auth:
        return ""
    parts = []
    for name, url in auth:
        if url:
            parts.append('<a href="%s" target="_blank" rel="noopener">%s</a>' % (e(url), e(name)))
        else:
            parts.append(e(name))
    if len(parts) == 1:
        joined = parts[0]
    elif len(parts) == 2:
        joined = parts[0] + " and " + parts[1]
    else:
        joined = ", ".join(parts[:-1]) + ", and " + parts[-1]
    return '<span class="coauthors">with %s</span>' % joined


def links_html(links):
    if not links:
        return ""
    out = []
    for label, url in links:
        ext = ' target="_blank" rel="noopener"' if url.startswith("http") else ""
        out.append("[<a href=\"%s\"%s>%s</a>]" % (e(url), ext, e(label)))
    return '<p class="paper-links">' + " ".join(out) + "</p>"


def paper_html(p):
    title = e(p["title"])
    if p.get("url"):
        title_html = '<a class="paper-link" href="%s" target="_blank" rel="noopener">%s</a>' % (
            e(p["url"]), title)
    else:
        title_html = title

    meta = []
    a = authors_html(p.get("authors"))
    if a:
        meta.append(a)
    if p.get("journal") and p.get("forthcoming"):
        meta.append('<span class="venue">Forthcoming, <em>%s</em></span>' % e(p["journal"]))
    elif p.get("journal"):
        meta.append('<span class="venue"><em>%s</em> (%s)</span>' % (e(p["journal"]), p["year"]))
    if p.get("status"):
        meta.append('<span class="status">%s</span>' % e(p["status"]))
    if p.get("note"):
        meta.append('<span class="note">%s</span>' % e(p["note"]))
    meta_html = '<p class="paper-meta">' + " &middot; ".join(meta) + "</p>" if meta else ""

    extra = ""
    if p.get("award"):
        extra += '\n        <p class="award">%s</p>' % e(p["award"])
    if p.get("presentations"):
        extra += ('\n        <p class="presentations">'
                  '<span>Selected presentations:</span> %s</p>' % e(p["presentations"]))

    abstract = ABS.get(p.get("key") or "")
    details = ""
    if abstract:
        abstract = abstract.strip()
        if abstract.lower().startswith("abstract "):
            abstract = abstract[9:]
        details = (
            '\n        <details class="abstract">'
            '\n          <summary>Abstract</summary>'
            '\n          <div class="abstract-body"><p>%s</p></div>'
            '\n        </details>' % e(abstract)
        )

    return (
        '\n      <article class="paper">'
        '\n        <h3 class="paper-title">%s</h3>'
        '\n        %s%s%s'
        '\n        %s'
        '\n      </article>' % (title_html, meta_html, extra, details, links_html(p.get("links")))
    )


def section(sid, heading, items):
    body = "".join(paper_html(p) for p in items)
    return ('\n    <section id="%s">'
            '\n      <h2>%s</h2>%s'
            '\n    </section>' % (sid, e(heading), body))


HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="author" content="Tobin Hanspal">
<link rel="canonical" href="https://tobinhanspal.github.io/{canon}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://tobinhanspal.github.io/{canon}">
<meta name="twitter:card" content="summary">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,400;0,700;1,400&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<div class="wrapper">
"""

SIDEBAR = """  <header class="sidebar">
    <h1 class="name"><a href="index.html">Tobin Hanspal</a></h1>
    <img class="portrait" src="assets/img/photo2.jpg" alt="Tobin Hanspal" onerror="this.remove()">
    <p class="role">Associate Professor of Finance<br>
      <a href="https://www.wu.ac.at/en/finance/people/faculty/tobin-hanspal" target="_blank" rel="noopener">WU Vienna University of Economics and Business</a>
    </p>
    <p class="affil">
      Faculty Member, <a href="https://www.vgsf.ac.at/" target="_blank" rel="noopener">Vienna Graduate School of Finance</a> (VGSF)<br>
      Research Affiliate, Leibniz Institute for Financial Research SAFE<br>
      Network Member, <a href="https://cepr.org/research/research-policy-networks/household-finance" target="_blank" rel="noopener">CEPR Household Finance Research Policy Network</a>
    </p>
    <p class="cv"><a class="btn" href="files/cv.pdf" target="_blank" rel="noopener">Curriculum Vitae (PDF)</a></p>
    <p class="logos">
      <a href="https://www.wu.ac.at/en/finance/people/faculty/tobin-hanspal" target="_blank" rel="noopener">
        <img class="logo logo-wu" src="assets/img/logo-wu.svg" width="71" height="38"
             alt="WU Vienna University of Economics and Business" loading="lazy">
      </a>
      <a href="https://www.vgsf.ac.at/" target="_blank" rel="noopener">
        <img class="logo logo-vgsf" src="assets/img/logo-vgsf.svg" width="95" height="24"
             alt="Vienna Graduate School of Finance" loading="lazy">
      </a>
    </p>
    <h2 class="side-h">Contact</h2>
    <p class="contact">
      <a href="mailto:tobin.hanspal@wu.ac.at">tobin.hanspal@wu.ac.at</a><br>
      +43 1 313 36 6371
    </p>
    <p class="address">
      Department of Finance, Accounting and Statistics<br>
      Institute for Finance, Banking and Insurance<br>
      WU Vienna University of Economics and Business<br>
      Welthandelsplatz 1<br>
      A-1020 Vienna, Austria
    </p>
  </header>
"""

FOOT = """  </main>
</div>
<footer class="site-footer">
  <div class="wrapper"><small>&copy; {year} Tobin Hanspal</small></div>
</footer>
</body>
</html>
"""

INDEX_DESC = ("Tobin Hanspal, Associate Professor of Finance at WU Vienna. Research in household "
              "finance, investor behavior, and the effect of personal experiences on financial decisions.")


def build_index():
    parts = [HEAD.format(title="Tobin Hanspal", desc=INDEX_DESC, canon="")]
    parts.append(SIDEBAR)
    parts.append('  <main id="main" class="content">\n')
    parts.append(section("current-research", "Current Research", WORKING))
    parts.append(section("publications", "Publications", PUBLICATIONS))
    parts.append(section("resting-papers", "Resting Papers", RESTING))
    parts.append(FOOT.format(year=2026))
    return "".join(parts)


SURVEY_BODY = """  <main id="main" class="content">
    <section id="appendix">
      <h2>Appendix Materials</h2>
      <p>Online appendix and survey instructions for
        <em>Exposure to the COVID-19 Stock Market Crash and its Effect on Household Expectations</em>
        (with <a href="https://sites.google.com/view/anniweber/" target="_blank" rel="noopener">Annika Weber</a>
        and <a href="https://sites.google.com/site/johanneswohlfartecon/home" target="_blank" rel="noopener">Johannes Wohlfart</a>,
        <em>Review of Economics and Statistics</em>, 2021).</p>
      <ul class="files">
        <li><a href="files/oappendix.pdf" target="_blank" rel="noopener">Online Appendix (PDF)</a></li>
        <li><a href="files/survey_instructions.pdf" target="_blank" rel="noopener">Survey Instructions (PDF)</a></li>
      </ul>
      <p class="back"><a href="index.html">&larr; Back to research</a></p>
    </section>
"""

SURVEY_DESC = ("Online appendix and survey instructions for Exposure to the COVID-19 Stock Market "
               "Crash and its Effect on Household Expectations.")


def build_survey():
    parts = [HEAD.format(title="Appendix Materials - Tobin Hanspal",
                         desc=SURVEY_DESC, canon="survey.html")]
    parts.append(SIDEBAR)
    parts.append(SURVEY_BODY)
    parts.append(FOOT.format(year=2026))
    return "".join(parts)


if __name__ == "__main__":
    for name, fn in (("index.html", build_index), ("survey.html", build_survey)):
        path = os.path.join(ROOT, name)
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(fn())
        print("wrote %s (%d bytes)" % (name, os.path.getsize(path)))
