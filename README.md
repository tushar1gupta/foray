# Foray

Marketing site for Foray, an engineering search firm placing early and mid-level
engineers at startups from seed through growth stage.

Live at **https://goforay.io** (Vercel project `goforay`).

Static HTML, no framework, no build step at deploy time. The pages are generated
from Python so the hero scene and the repeated chrome stay in one place.

## Structure

```
index.html          landing page
companies.html      onboarding: post a role
engineers.html      onboarding: join the pool
404.html
style.css           shared, extracted at build time
app.js              shared, extracted at build time
og.png              1200x630 share card, generated
favicon.svg
robots.txt          generated
sitemap.xml         generated
vercel.json         clean URLs, security headers, asset caching
src/
  generate.py       builds the four HTML pages
  scene.py          the hero scene: glyph field, tower, walk cycle
  configure.py      stamps the domain, writes assets, extracts css/js
  check.py          audit: structure, links, copy, forms, JS syntax
```

## Build

Requires Python 3.11+, Pillow (for the share card), and Node (for the JS syntax
check only).

```bash
cd src
python3 generate.py                                  # write the HTML
python3 configure.py goforay.io contact@goforay.io   # stamp domain, emit assets
python3 check.py                                     # audit, must report no errors
```

`configure.py` is idempotent. Run it again with a different domain or contact
address and everything downstream updates: canonical tags, Open Graph tags,
`robots.txt`, `sitemap.xml`, and every `mailto:` on the site.

A clean rebuild is byte-identical to the previous one. Nothing depends on the
current time or a random seed at build time.

## Deploy

Vercel serves the repo root as static files. No build command, no output
directory, framework preset **Other**.

```bash
npx vercel --prod
```

`.vercelignore` keeps `src/` out of the deployment.

## The hero scene

The right half of the landing page is a monospace grid, 122 x 64 cells.

- **Static layer** — ambient glyph noise, a ground line, and a tower with lit
  windows. Deterministic from a seed, so `app.js` generates it in the browser
  rather than shipping 36 KB of markup. The JS port is verified byte-identical
  to `scene.py`.
- **Walkers** — two figures rasterised from a joint model. Hip and shoulder
  angles are sinusoids of the walk phase, the knee flexes only on the backswing,
  and limb glyphs are chosen from each segment's true screen angle after
  correcting for the 0.6 cell aspect ratio. Ten frames, swapped every 95 ms.
- **Absorption** — when a figure reaches the doorway it fades, and one more
  window lights permanently. Capped at 26 so the facade never washes out.

Everything freezes into a sensible still under `prefers-reduced-motion`.

## Before this is really live

The following is placeholder content and needs to be replaced or removed:

- [ ] **The three testimonials on `index.html` are invented.** They are
      attributed to unnamed founders. Replace them with real quotes or delete
      the "What Founders Say" section.
- [ ] **"Fifteen Hundred Profiles, Five Introductions"** and the five profile
      strings behind the screen bar in `app.js` are illustrative.
- [ ] **The forms open the visitor's mail client** via `mailto:`. On a phone
      with no mail app configured the button does nothing and the submission is
      lost silently. Move both intakes to a real endpoint before driving any
      traffic here.
- [ ] **`contact@goforay.io` must be a mailbox that exists.** Every CTA and both
      forms point at it.
- [ ] Confirm the claims the copy makes are ones the business actually keeps:
      same-day reply, first introductions inside two weeks, a senior engineer
      reading every candidate's code, no fee unless placed.
