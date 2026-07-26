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
}

FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
<rect width="32" height="32" rx="6" fill="#080D0B"/>
<rect x="9" y="9" width="6" height="6" rx="1.4" fill="#5FE4CE"/>
<rect x="17" y="9" width="6" height="6" rx="1.4" fill="#5FE4CE" opacity=".45"/>
<rect x="9" y="17" width="6" height="6" rx="1.4" fill="#5FE4CE" opacity=".35"/>
<rect x="17" y="17" width="6" height="6" rx="1.4" fill="#5FE4CE" opacity=".8"/>
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
    BG, MUT, MINT, TEXT, DIM = "#080D0B", "#8DA29B", "#5FE4CE", "#E6EDE9", "#141C19"
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    sans = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 64)
    small = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 20)
    tiny = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 22)

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
                        fill=MINT if (row, col) in lit else "#243330")
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
    d.text((64, 236), "Foray into", font=sans, fill=TEXT)
    d.text((64, 312), "your next hire.", font=sans, fill=TEXT)
    d.rectangle([64, 410, 150, 412], fill=MINT)
    d.text((64, 440), "Early and mid-level engineering", font=tiny, fill=MUT)
    d.text((64, 472), "search for startups.", font=tiny, fill=MUT)
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
<meta name="theme-color" content="#080D0B">
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

    # 404 built from the real shell so it is not a bare Vercel page
    idx = (SITE / "index.html").read_text(encoding="utf-8")
    head = idx[:idx.index("<main>")]
    tail = idx[idx.index("<footer>"):]
    head = head.replace("<title>Foray | Engineering search for startups</title>",
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


def externalise():
    """Pull the duplicated <style> and <script> into shared cached files."""
    css = js = None
    for f in sorted(SITE.glob("*.html")):
        s = f.read_text(encoding="utf-8")
        m_css = re.search(r"<style>([\s\S]*?)</style>", s)
        m_js = re.search(r"<script>([\s\S]*?)</script>", s)
        if m_css and css is None:
            css = m_css.group(1)
        if m_js and js is None:
            js = m_js.group(1)
        if m_css:
            s = s.replace(m_css.group(0), '<link rel="stylesheet" href="/style.css">')
        if m_js:
            s = s.replace(m_js.group(0), '<script src="/app.js" defer></script>')
        f.write_text(s, encoding="utf-8")
    if css:
        # strip comments and collapse the indentation the source uses for readability
        css = re.sub(r"/\*[\s\S]*?\*/", "", css)
        css = re.sub(r"\n\s+", "\n", css)
        css = re.sub(r"\n{2,}", "\n", css).strip()
        (SITE / "style.css").write_text(css, encoding="utf-8")
    if js:
        (SITE / "app.js").write_text(js.strip(), encoding="utf-8")
    print(f"  extracted style.css ({len(css)//1024} KB) and app.js ({len(js)//1024} KB)")


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
