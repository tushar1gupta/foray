#!/usr/bin/env python3
"""Builds the Foray site.

Writes index.html, candidates.html, privacy.html, terms.html and 404.html to the
repo root. Bodies come from company.py, candidate.py and legal.py; landing.py is
the shared shell around them, and this module is the table of what gets written.

index.html is the COMPANY page. It used to be the candidate landing page, which
is now parked in src/parked/candidates.py -- see that file for why. /companies
and /engineers redirect in vercel.json, so old links still land.

Run src/configure.py afterwards to stamp the domain and emit the static assets.
"""
import pathlib
from landing import CSS as LP_CSS, legal_shell, head_bar, foot
from company import CSS as CO_CSS, JS as CO_JS, body as company_body
from candidate import CSS as CA_CSS, JS as CA_JS, body as candidate_body
from legal import PRIVACY_H1, PRIVACY_BODY, TERMS_H1, TERMS_BODY

OUT = pathlib.Path(__file__).resolve().parent.parent
OUT.mkdir(parents=True, exist_ok=True)







LANDING_FONTS = ("https://fonts.googleapis.com/css2?"
                 "family=Bricolage+Grotesque:wght@500;600;700"
                 "&family=Schibsted+Grotesk:wght@400;500;600&display=swap")


def page(title, desc, css, body, js):
    """Every generated page except the legal ones: shared shell, own body.

    LP_CSS rides along with the page's own: the palette, the buttons and the
    cards all come from landing.py, and each page adds only what is specific
    to it.
    """
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{LANDING_FONTS}" rel="stylesheet">
<style>{LP_CSS}{css}</style>
<script>
  window.va = window.va || function () {{ (window.vaq = window.vaq || []).push(arguments); }};
</script>
<script defer src="/_vercel/insights/script.js"></script>
</head>
<body>
{body}
<script data-page>{js}</script>
</body>
</html>
"""


def notfound():
    """Generated, not spliced. The old 404 took its head from another page and
    inherited that page's canonical tag along with it."""
    body = (
        '<div class="lp">\n\n'
        + head_bar(None)
        + '''
  <main class="lp-legal">
    <span class="lbl" style="color:var(--primary)">404</span>
    <h1>That page does not exist.</h1>
    <div class="body">
      <p>It may have moved. These are the ones that are here.</p>
      <p style="display:flex; flex-wrap:wrap; gap:12px; margin-top:22px">
        <a class="lp-btn" href="index.html">Send us a role</a>
        <a class="lp-btn ghost" href="candidates.html">For candidates</a>
      </p>
    </div>
  </main>

'''
        + foot(None)
        + '</div>\n'
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page not found | Foray</title>
<meta name="description" content="That page does not exist. Foray is a recruiting agency for startups, seed through growth stage.">
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{LANDING_FONTS}" rel="stylesheet">
<style>{LP_CSS}</style>
</head>
<body>
{body}
</body>
</html>
"""


def legal(title, desc, h1, prose):
    """A legal page: the landing chrome and palette, and no script at all."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{LANDING_FONTS}" rel="stylesheet">
<style>{LP_CSS}</style>
<script>
  window.va = window.va || function () {{ (window.vaq = window.vaq || []).push(arguments); }};
</script>
<script defer src="/_vercel/insights/script.js"></script>
</head>
<body>
{legal_shell(h1, prose)}
</body>
</html>
"""


pages = {
    "index.html": ("Foray | Recruiting for startups",
                   "Foray is a recruiting agency for startups, seed through growth stage. "
                   "Send us a role and we bring you five candidates worth interviewing. "
                   "Success fee only, nothing until you hire."),
    "candidates.html": ("For candidates | Foray",
                        "Tell us what you want next and we will keep you in mind for the "
                        "searches we run. Free for you, always."),
    "privacy.html": ("Privacy Policy | Foray",
                     "How GoForay, Co. collects, uses, and protects the information "
                     "candidates and companies give us."),
    "terms.html": ("Terms of Service | Foray",
                   "The agreement between you and GoForay, Co. when you use Foray."),
}

for name, (title, desc) in pages.items():
    if name == "index.html":
        html = page(title, desc, CO_CSS, company_body(), CO_JS)
    elif name == "candidates.html":
        html = page(title, desc, CO_CSS + CA_CSS, candidate_body(), CA_JS)
    elif name == "privacy.html":
        html = legal(title, desc, PRIVACY_H1, PRIVACY_BODY)
    else:
        html = legal(title, desc, TERMS_H1, TERMS_BODY)
    (OUT / name).write_text(html, encoding="utf-8")
    print("wrote", name, f"{len((OUT / name).read_text(encoding='utf-8')) // 1024} KB")

# companies.html was the old home of what is now index.html. Vercel redirects
# /companies -> /, but the stale FILE would win over the redirect, so it goes.
stale = OUT / "companies.html"
if stale.exists():
    stale.unlink()
    print("removed companies.html (now redirected to /)")

(OUT / "404.html").write_text(notfound(), encoding="utf-8")
print("wrote 404.html")
