#!/usr/bin/env python3
"""Static audit of the Foray build: structure, links, CSS, copy, a11y."""
import re, pathlib
from html.parser import HTMLParser

SITE = pathlib.Path(__file__).resolve().parent.parent
FILES = sorted(SITE.glob("*.html"))
VOID = {"area","base","br","col","embed","hr","img","input","link","meta",
        "param","source","track","wbr"}
issues, notes = [], []


def log(f, msg):
    issues.append(f"{f}: {msg}")


class Structure(HTMLParser):
    def __init__(self, f):
        super().__init__(convert_charrefs=True)
        self.f, self.stack, self.ids, self.text = f, [], [], []
        self.imgs_no_alt = 0
        self.a_no_text = 0
        self._in_a = False
        self._a_text = ""

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "img" and not a.get("alt"):
            self.imgs_no_alt += 1
        if tag == "a":
            self._in_a = True
            self._a_text = a.get("aria-label", "")
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag == "a":
            if not self._a_text.strip():
                self.a_no_text += 1
            self._in_a = False
        if tag in VOID:
            return
        if not self.stack:
            log(self.f, f"stray </{tag}> at line {self.getpos()[0]}")
            return
        top, line = self.stack.pop()
        if top != tag:
            log(self.f, f"mismatched tag: <{top}> opened line {line}, closed as </{tag}> "
                        f"line {self.getpos()[0]}")

    def handle_data(self, d):
        self.text.append(d)
        if self._in_a:
            self._a_text += d


all_text = {}
all_ids = {}
hrefs = {}

for p in FILES:
    src = p.read_text(encoding="utf-8")
    par = Structure(p.name)
    par.feed(src)
    if par.stack:
        for tag, line in par.stack:
            log(p.name, f"unclosed <{tag}> opened at line {line}")

    dupes = {i for i in par.ids if par.ids.count(i) > 1}
    if dupes:
        log(p.name, f"duplicate id(s): {sorted(dupes)}")
    all_ids[p.name] = set(par.ids)

    # strip script/style before copy checks
    body = re.sub(r"<(script|style|pre)[\s\S]*?</\1>", " ", src, flags=re.I)
    all_text[p.name] = re.sub(r"<[^>]+>", " ", body)

    hrefs[p.name] = re.findall(r'href="([^"]+)"', src)

    if not re.search(r"<style>", src):
        for _need in ('href="/style.css"', 'src="/app.js"'):
            if _need not in src:
                log(p.name, f"missing {_need}")

    # required head elements
    for need, label in [(r"<html lang=", "lang attribute"),
                        (r'name="viewport"', "viewport meta"),
                        (r'name="description"', "meta description"),
                        (r"<title>", "title")]:
        if not re.search(need, src):
            log(p.name, f"missing {label}")

    # exactly one h1 on the homepage, none required elsewhere
    h1s = len(re.findall(r"<h1[ >]", src))
    if h1s != 1:
        log(p.name, f"expected exactly 1 <h1>, found {h1s}")

    if par.imgs_no_alt:
        log(p.name, f"{par.imgs_no_alt} img without alt")
    if par.a_no_text:
        log(p.name, f"{par.a_no_text} link(s) with no text or aria-label")

# ---- link integrity
pagenames = {p.name for p in FILES}
for f, hs in hrefs.items():
    for h in hs:
        if h.startswith("mailto:"):
            if not re.match(r"mailto:contact@goforay\.(ai|io)$", h):
                log(f, f"wrong email in {h}")
        elif h.startswith("#"):
            if h[1:] and h[1:] not in all_ids[f]:
                log(f, f"anchor {h} has no target")
        elif h.startswith("http"):
            if "fonts.g" not in h:
                notes.append(f"{f}: external link {h}")
        else:
            target = h.split("#")[0].split("?")[0]
            root = SITE
            if target.startswith("/"):
                target = target[1:]                     # root-relative
            candidates = [target, target + ".html"]     # vercel cleanUrls
            if target and not any((root / c2).exists() for c2 in candidates):
                log(f, f"broken internal link -> {h}")
            frag = h.split("#")[1] if "#" in h else ""
            _tk = target if target.endswith(".html") else target + ".html"
            if frag and _tk in all_ids and frag not in all_ids.get(_tk, set()):
                log(f, f"link {h} points at a missing anchor")

# every page reachable from index
reach = {t.split("#")[0] for t in hrefs["index.html"] if not t.startswith(("mailto:", "http", "#"))}
for name in pagenames - {"index.html"}:
    if name not in reach:
        notes.append(f"index.html does not link directly to {name}")

# ---- CSS sanity (shared block, check once)
_ext_css = SITE / "style.css"
if _ext_css.exists():
    css = _ext_css.read_text(encoding="utf-8")
else:
    css = re.search(r"<style>([\s\S]*?)</style>", FILES[0].read_text(encoding="utf-8")).group(1)
if css.count("{") != css.count("}"):
    log("css", f"unbalanced braces: {css.count('{')} open vs {css.count('}')} close")
declared = set(re.findall(r"(--[a-z0-9-]+)\s*:", css))
used = set(re.findall(r"var\((--[a-z0-9-]+)", css))
missing = used - declared
if missing:
    log("css", f"var() with no declaration: {sorted(missing)}")
unused = declared - used
if unused:
    notes.append(f"css: declared but unused: {sorted(unused)}")

# selectors defined in css but never used in markup
markup = " ".join(p.read_text(encoding="utf-8") for p in FILES)
JS_CLASSES = {"tick", "hit", "in", "kept", "on", "prefilled", "prefilled-card"}
for cls in sorted(set(re.findall(r"\.([a-z][a-z0-9-]{1,14})[\s,{:>.]", css)) - JS_CLASSES):
    if f'class="' in markup and not re.search(r'class="[^"]*\b%s\b' % re.escape(cls), markup):
        notes.append(f"css: .{cls} never used in markup")

# cream/warm-background leftovers
for hexv in re.findall(r"#[0-9A-Fa-f]{6}", css):
    r, g, b = (int(hexv[i:i+2], 16) for i in (1, 3, 5))
    if r > 200 and g > 195 and b < g - 6 and r > b + 8:   # warm = red exceeds blue
        log("css", f"warm/cream tone still present: {hexv}")

# forms must not be real <form> elements: there is no backend to submit to
for _f in FILES:
    _s = _f.read_text(encoding="utf-8")
    if re.search(r"<form[ >]", _s):
        log(_f.name, "raw <form> element would submit with no backend")
    # every field needs a label and a data-label for the composed email
    _lab = set(re.findall(r'<label for="([\w-]+)"', _s))
    _unlabelled = []
    for _tag in re.findall(r"<(?:input|textarea|select)\b[^>]*>", _s):
        _id = re.search(r'id="([\w-]+)"', _tag)
        if "aria-label" in _tag:
            continue                      # aria-label is a valid alternative
        if not _id or _id.group(1) not in _lab:
            _unlabelled.append(_id.group(1) if _id else _tag[:40])
    if _unlabelled:
        log(_f.name, f"fields with no label and no aria-label: {_unlabelled}")
    _n_fields = len(re.findall(r"<(?:input|textarea|select)\b", _s))
    _n_dl = len(re.findall(r'data-label="', _s))
    if _n_fields and "data-compose" in _s and _n_dl < _n_fields - 1:
        log(_f.name, f"{_n_fields - _n_dl} fields missing data-label")

# tab panels: exactly one selected tab and one visible panel per page
for _f in FILES:
    _s = _f.read_text(encoding="utf-8")
    _tabs = re.findall(r'role="tab" data-panel="(\w+)" aria-selected="(\w+)"', _s)
    if not _tabs:
        continue
    _sel = [a for _, a in _tabs if a == "true"]
    _panels = re.findall(r'<div class="panel" data-panel="(\w+)"( hidden)?>', _s)
    if len(_sel) != 1:
        log(_f.name, f"{len(_sel)} tabs marked selected")
    if len(_panels) != len(_tabs):
        log(_f.name, f"{len(_tabs)} tabs but {len(_panels)} panels")
    if sum(1 for _, h in _panels if h) != len(_panels) - 1:
        log(_f.name, "exactly one panel should be visible on load")

# ---- copy checks
BANNED = ["genuinely","truly","really","very","actually","seamless","seamlessly","robust",
          "cutting-edge","world-class","best-in-class","leverage","unlock","synergy",
          "passionate","incredibly","deeply","journey","game-changing","revolutionary",
          "elevate","empower","holistic","bespoke","curated","state-of-the-art"]
for f, t in all_text.items():
    low = t.lower()
    for w in BANNED:
        for m in re.finditer(r"\b" + re.escape(w) + r"\b", low):
            log(f, f'filler/flare word "{w}" near: ...{t[max(0,m.start()-34):m.start()+len(w)+26].strip()}...')
    if "\u2014" in t:
        log(f, "em dash in copy")
    if "\u2013" in t:
        notes.append(f"{f}: en dash present (numeric range, intentional)")
    for m in re.finditer(r"\b(\w+) \1\b", low):
        if m.group(1) not in ("that",):
            log(f, f'repeated word "{m.group(1)} {m.group(1)}"')

# font families actually referenced
fams = set(re.findall(r"font-family:([^;}]+)", css))
notes.append("css: font-family declarations -> " + " | ".join(sorted(f.strip() for f in fams)))
gf = set(re.findall(r"family=([A-Za-z+]+)", markup))
notes.append("fonts loaded -> " + ", ".join(sorted(gf)))

# word count per page
for f, t in all_text.items():
    notes.append(f"{f}: {len(t.split())} words")

# inline JS must actually parse, and embedded frame data must survive escaping
import subprocess, tempfile, json as _json
for _f in FILES:
    _s = _f.read_text(encoding="utf-8")
    _m = re.search(r"<script>([\s\S]*?)</script>", _s)
    _ext_js = SITE / "app.js"
    if not _m and _ext_js.exists():
        class _Shim:
            def group(self, _n): return _ext_js.read_text(encoding="utf-8")
        _m = _Shim()
    if not _m:
        continue
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as _t:
        _t.write(_m.group(1)); _p = _t.name
    _r = subprocess.run(["node", "--check", _p], capture_output=True, text=True)
    if _r.returncode:
        log(_f.name, "inline JS syntax error: " + _r.stderr.strip().split("\n")[-1])
    _fr = re.search(r"var FRAMES=(\[[\s\S]*?\]);", _m.group(1))
    if _fr:
        try:
            _frames = _json.loads(_fr.group(1))
            if any("\\n" in x for x in _frames):
                log(_f.name, "frame data contains literal backslash-n instead of newlines")
            if len({len(x.split(chr(10))) for x in _frames}) != 1:
                log(_f.name, "frames have inconsistent heights")
        except Exception as _e:
            log(_f.name, f"frame data will not parse as JSON: {_e}")

print("=" * 62)
print("ERRORS")
print("=" * 62)
print("\n".join(issues) if issues else "none")
print()
print("=" * 62)
print("NOTES")
print("=" * 62)
print("\n".join(notes))
