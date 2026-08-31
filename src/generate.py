#!/usr/bin/env python3
"""Builds the Foray site.

Writes index.html, companies.html, privacy.html, terms.html and 404.html to the
repo root. Bodies come from landing.py, company.py and legal.py; this module is
the shell around them and the table of what gets written.

Run src/configure.py afterwards to stamp the domain and emit the static assets.
"""
import pathlib
from landing import CSS as LP_CSS, JS as LP_JS, BODY as LP_BODY, legal_shell
from company import CSS as CO_CSS, JS as CO_JS, body as company_body
from landing import head_bar, foot
from legal import PRIVACY_H1, PRIVACY_BODY, TERMS_H1, TERMS_BODY

OUT = pathlib.Path(__file__).resolve().parent.parent
OUT.mkdir(parents=True, exist_ok=True)







LANDING_FONTS = ("https://fonts.googleapis.com/css2?"
                 "family=Bricolage+Grotesque:wght@500;600;700"
                 "&family=Schibsted+Grotesk:wght@400;500;600&display=swap")


def landing(title, desc):
    """index.html: its own chrome, its own palette, its own script."""
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
{LP_BODY}
<script data-page>{LP_JS}</script>
</body>
</html>
"""

def company(title, desc):
    """The company page. Same shell as the landing page, its own body and script.

    It carries LP_CSS as well as its own: the palette, the buttons and the band
    all come from landing.py, and this only adds what is specific to the page.
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
<style>{LP_CSS}{CO_CSS}</style>
<script>
  window.va = window.va || function () {{ (window.vaq = window.vaq || []).push(arguments); }};
</script>
<script defer src="/_vercel/insights/script.js"></script>
</head>
<body>
{company_body()}
<script data-page>{CO_JS}</script>
</body>
</html>
"""


def notfound():
    """Generated, not spliced. The old 404 took its head from companies.html and
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
        <a class="lp-btn" href="index.html">For candidates</a>
        <a class="lp-btn ghost" href="companies.html">For companies</a>
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
<meta name="description" content="That page does not exist. Foray finds engineering roles for candidates and pre-interviewed engineers for companies.">
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
    "index.html": ("Foray | Your autonomous recruiting agent",
                   "Message Foray and we find roles worth your time, write the application, and apply for you. A human reviews everything, and nothing sends without your yes."),
    "privacy.html": ("Privacy Policy | Foray",
                     "How GoForay, Co. collects, uses, and protects the information "
                     "engineers and companies give us."),
    "terms.html": ("Terms of Service | Foray",
                   "The agreement between you and GoForay, Co. when you use Foray."),
    "companies.html": ("Hiring engineers | Foray",
                       "Send us the role and we come back within a day with five pre-interviewed "
                       "engineers and our read on each. Success fee only, nothing until you hire."),
}

for name, (title, desc) in pages.items():
    if name == "index.html":
        html = landing(title, desc)
    elif name == "privacy.html":
        html = legal(title, desc, PRIVACY_H1, PRIVACY_BODY)
    elif name == "terms.html":
        html = legal(title, desc, TERMS_H1, TERMS_BODY)
    else:
        html = company(title, desc)
    (OUT / name).write_text(html, encoding="utf-8")
    print("wrote", name, f"{len((OUT / name).read_text(encoding='utf-8')) // 1024} KB")

(OUT / "404.html").write_text(notfound(), encoding="utf-8")
print("wrote 404.html")
