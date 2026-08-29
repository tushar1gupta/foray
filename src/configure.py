#!/usr/bin/env python3
"""Production configuration for the Foray site.

Usage:
    python3 configure.py <domain> [contact-email]

Example:
    python3 configure.py foray.ai contact@foray.ai

Stamps the domain into canonical tags, Open Graph tags, robots.txt and the
sitemap, replaces the contact email everywhere, and writes the supporting files
Vercel needs. Idempotent: safe to run again with a different domain.
"""
import re
import sys
import pathlib

SITE = pathlib.Path(__file__).resolve().parent.parent
PAGES = {
    "index.html": ("Foray | Engineering search for startups",
                   "Foray runs early and mid-level engineering searches for startups from seed "
                   "through growth stage."),
    "companies.html": ("For companies | Foray",
                       "Post an engineering role to Foray. Paste your job description and we reply "
                       "within a day."),
    "engineers.html": ("For engineers | Foray",
                       "Join the Foray pool with your LinkedIn and GitHub. We contact you only when "
                       "a role fits."),
    # Hand-written rather than generated, but they still want a canonical tag,
    # the share card and a place in the sitemap.
    "privacy.html": ("Privacy policy | Foray",
                     "How Foray collects, uses and stores the details you give us."),
    "terms.html": ("Terms of service | Foray",
                   "The terms you agree to when you use Foray."),
}

FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
<rect width="32" height="32" rx="6" fill="#241C3B"/>
<rect x="9" y="9" width="6" height="6" rx="1.4" fill="#9B7FE0"/>
<rect x="17" y="9" width="6" height="6" rx="1.4" fill="#9B7FE0" opacity=".45"/>
<rect x="9" y="17" width="6" height="6" rx="1.4" fill="#9B7FE0" opacity=".35"/>
<rect x="17" y="17" width="6" height="6" rx="1.4" fill="#9B7FE0" opacity=".8"/>
</svg>
"""

VERCEL_JSON = """{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "cleanUrls": true,
  "trailingSlash": false,
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "SAMEORIGIN" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" },
        { "key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=()" }
      ]
    },
    {
      "source": "/(.*)\\\\.(svg|png|ico|woff2)",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
      ]
    }
  ]
}
"""


def og_card(domain):
    """1200x630 share card. Flat shapes only, so the PNG stays a few KB."""
    from PIL import Image, ImageDraw, ImageFont

    W, H = 1200, 630
    BG, MUT, MINT, TEXT, DIM = "#241C3B", "#9B8FB8", "#B9A2F0", "#F4F1FA", "#2E2547"
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    def font(bold, size):
        names = (["/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
                  "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                  "C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/segoeuib.ttf",
                  "/System/Library/Fonts/Supplemental/Arial Bold.ttf"] if bold else
                 ["/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
                  "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                  "C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/segoeui.ttf",
                  "/System/Library/Fonts/Supplemental/Arial.ttf"])
        for n in names:
            try:
                return ImageFont.truetype(n, size)
            except OSError:
                continue
        return ImageFont.load_default()

    sans, small, tiny = font(True, 64), font(True, 20), font(False, 22)

    # right side: a tower and a figure walking into the lit doorway
    bx0, bx1, by0, by1 = 800, 1080, 150, 520
    d.rectangle([bx0, by0, bx1, by1], fill=DIM)
    d.rectangle([bx0, by0, bx1, by0 + 3], fill=MUT)
    d.rectangle([bx0, by0, bx0 + 2, by1], fill=MUT)
    d.rectangle([bx1 - 2, by0, bx1, by1], fill=MUT)
    d.rectangle([938, 96, 941, 150], fill=MUT)
    d.rectangle([932, 88, 947, 98], fill=MINT)
    lit = {(0, 1), (1, 0), (1, 3), (2, 2), (3, 0), (3, 3), (4, 1), (5, 2), (5, 4), (6, 0)}
    for row in range(8):
        for col in range(5):
            x, y = bx0 + 26 + col * 52, by0 + 30 + row * 42
            d.rectangle([x, y, x + 30, y + 20],
                        fill=MINT if (row, col) in lit else "#332A4D")
    d.rectangle([916, 440, 966, 520], fill=MINT)         # doorway
    d.rectangle([680, 518, 1120, 521], fill=MUT)          # ground
    # figure: head, torso, legs mid-stride
    d.ellipse([846, 452, 862, 470], fill=MINT)
    d.rectangle([850, 472, 858, 500], fill=MINT)
    d.line([(854, 500), (840, 518)], fill=MINT, width=5)
    d.line([(854, 500), (870, 518)], fill=MINT, width=5)
    d.line([(852, 480), (838, 496)], fill=MINT, width=4)

    # left side: type
    d.rectangle([64, 92, 92, 106], fill=MINT)
    d.text((104, 84), "FORAY", font=small, fill=TEXT)
    d.text((64, 236), "Your autonomous", font=sans, fill=TEXT)
    d.text((64, 312), "recruiting agent.", font=sans, fill=TEXT)
    d.rectangle([64, 410, 150, 412], fill=MINT)
    d.text((64, 440), "We find the roles, write the application,", font=tiny, fill=MUT)
    d.text((64, 472), "and apply for you.", font=tiny, fill=MUT)
    d.text((64, 540), domain, font=tiny, fill=MINT)

    img = img.convert("P", palette=Image.ADAPTIVE, colors=8)
    img.save(SITE / "og.png", optimize=True)
    return (SITE / "og.png").stat().st_size


def stamp(domain, email):
    base = f"https://{domain}"
    for name, (title, desc) in PAGES.items():
        f = SITE / name
        if not f.exists():
            print(f"  skip {name} (missing)")
            continue
        s = f.read_text(encoding="utf-8")
        slug = "" if name == "index.html" else "/" + name.replace(".html", "")
        url = base + (slug or "/")

        # drop any previous stamp so re-running is clean
        s = re.sub(r'\n<link rel="canonical"[\s\S]*?<!-- /stamp -->', "", s)
        block = f"""
<link rel="canonical" href="{url}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Foray">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{base}/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{base}/og.png">
<meta name="theme-color" content="#241C3B">
<!-- /stamp -->"""
        s = s.replace('<link rel="preconnect" href="https://fonts.googleapis.com">',
                      block + '\n<link rel="preconnect" href="https://fonts.googleapis.com">', 1)

        # only the contact address, never the illustrative placeholders in form fields
        s = re.sub(r"contact@goforay\.(ai|io)", email, s)
        f.write_text(s, encoding="utf-8")
        print(f"  stamped {name} -> {url}")

    (SITE / "favicon.svg").write_text(FAVICON, encoding="utf-8")
    (SITE / "vercel.json").write_text(VERCEL_JSON, encoding="utf-8")
    (SITE / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {base}/sitemap.xml\n", encoding="utf-8")

    urls = "".join(
        f"  <url><loc>{base}{'' if n == 'index.html' else '/' + n.replace('.html','')}"
        f"{'/' if n == 'index.html' else ''}</loc>"
        f"<changefreq>monthly</changefreq>"
        f"<priority>{'1.0' if n == 'index.html' else '0.8'}</priority></url>\n"
        for n in PAGES if (SITE / n).exists())
    (SITE / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}</urlset>\n", encoding="utf-8")

    # 404 built from a real shell so it is not a bare Vercel page. Spliced from
    # companies.html rather than index: the landing page carries its own chrome
    # and stylesheet, and the 404 body below is written against the shared one.
    idx = (SITE / "companies.html").read_text(encoding="utf-8")
    head = idx[:idx.index("<main>")]
    tail = idx[idx.index("<footer>"):]
    head = head.replace("<title>For companies | Foray</title>",
                        "<title>Page not found | Foray</title>")
    (SITE / "404.html").write_text(head + """<main>
  <section class="sec first">
    <div class="wrap">
      <div class="head">
        <p class="lbl dim">404</p>
        <div>
          <h1 class="t2">That Page Does Not Exist.</h1>
          <p class="lede">It may have moved. These are the ones that are here.</p>
          <div class="acts">
            <a href="/companies" class="btn">Post a role</a>
            <a href="/engineers" class="btn ghost">Join the pool</a>
          </div>
        </div>
      </div>
    </div>
  </section>
</main>
""" + tail, encoding="utf-8")
    print("  wrote favicon.svg, vercel.json, robots.txt, sitemap.xml, 404.html")


COMMENT_RE = re.compile(r"/\*[\s\S]*?\*/")
INDENT_RE = re.compile(r"\n\s+")
BLANKS_RE = re.compile(r"\n{2,}")
STYLE_RE = re.compile(r"<style>([\s\S]*?)</style>")
# The page script carries data-page. The analytics tag is also an inline
# <script>, and it now comes first in the document, so an unqualified match
# extracts the vendor shim and leaves the real script inline.
SCRIPT_RE = re.compile(r"<script data-page>([\s\S]*?)</script>")


def externalise():
    """Pull the inline <style>/<script> into cached files.

    Two pairs, not one: the three form pages share a stylesheet, and the landing
    page has its own. They have no rules in common, so folding them together
    would make every page pay for both -- and, worse, whichever page was walked
    first used to win, which silently handed the landing page the form pages'
    styles. The landing page is matched by name because it is the only one built
    by ``landing.py``.
    """
    def tidy(css):
        css = re.sub(COMMENT_RE, "", css)
        css = re.sub(INDENT_RE, chr(10), css)
        return re.sub(BLANKS_RE, chr(10), css).strip()

    shared_css = shared_js = None
    wrote = []
    for f in sorted(SITE.glob("*.html")):
        page = f.read_text(encoding="utf-8")
        m_css = re.search(STYLE_RE, page)
        m_js = re.search(SCRIPT_RE, page)
        is_landing = f.name == "index.html"

        if m_css:
            if is_landing:
                (SITE / "landing.css").write_text(tidy(m_css.group(1)), encoding="utf-8")
                wrote.append("landing.css")
            elif shared_css is None:
                shared_css = m_css.group(1)
            href = "/landing.css" if is_landing else "/style.css"
            page = page.replace(m_css.group(0),
                                '<link rel="stylesheet" href="%s">' % href)
        if m_js:
            if is_landing:
                (SITE / "landing.js").write_text(m_js.group(1).strip(), encoding="utf-8")
                wrote.append("landing.js")
            elif shared_js is None:
                shared_js = m_js.group(1)
            src = "/landing.js" if is_landing else "/app.js"
            page = page.replace(m_js.group(0),
                                '<script src="%s" defer></script>' % src)
        f.write_text(page, encoding="utf-8")

    if shared_css:
        (SITE / "style.css").write_text(tidy(shared_css), encoding="utf-8")
        wrote.append("style.css")
    if shared_js:
        (SITE / "app.js").write_text(shared_js.strip(), encoding="utf-8")
        wrote.append("app.js")
    sizes = ", ".join("%s (%d KB)" % (n, (SITE / n).stat().st_size // 1024) for n in wrote)
    print("  extracted " + sizes)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    dom = sys.argv[1].replace("https://", "").replace("http://", "").strip("/")
    mail = sys.argv[2] if len(sys.argv) > 2 else f"contact@{dom}"
    print(f"configuring for {dom}, contact {mail}")
    stamp(dom, mail)
    print(f"  og.png {og_card(dom) // 1024} KB")
    externalise()
    print("done")
