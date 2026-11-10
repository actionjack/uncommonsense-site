#!/usr/bin/env python3
"""Build the writing pages from posts/*.md. Standard library only.

Each posts/<slug>.md starts with a front-matter block:

    ---
    title: The log that cannot be edited afterwards
    date: 2026-09-29
    tag: AI governance
    description: One sentence for search results (155 characters or fewer).
    image: log-that-cannot-be-edited.jpg      (optional, in assets/writing/)
    alt: What the image shows.                 (required if image is set)
    linkedin: https://www.linkedin.com/feed/update/urn:li:activity:.../  (optional)
    ---
    Post text. Blank lines separate paragraphs. Lines starting "- " or "* " become a list.

Run: python3 build.py
Writes writing/<slug>/index.html, writing/index.html, the three newest cards in index.html,
sitemap.xml and the Writing section of llms.txt.
"""
import html
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = "https://uncommonsense-uk.com"
CALENDLY = "https://calendly.com/martin-uncommonsense-uk/30min"
LONG_DASH = chr(8212)
BULLET = chr(8226)


def parse(path):
    raw = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n(.*)", raw, re.S)
    if not m:
        raise SystemExit(f"{path.name}: missing front matter")
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    for key in ("title", "date", "tag", "description"):
        if not meta.get(key):
            raise SystemExit(f"{path.name}: front matter needs {key}")
    if meta.get("image") and not meta.get("alt"):
        raise SystemExit(f"{path.name}: image needs alt text")
    if LONG_DASH in raw:
        raise SystemExit(f"{path.name}: contains a long dash")
    meta["slug"] = path.stem
    meta["body"] = m.group(2).strip()
    meta["d"] = date.fromisoformat(meta["date"])
    return meta


def inline(text):
    out = html.escape(text, quote=False)
    out = re.sub(r"(https?://[^\s<]+[^\s<.,;:!?)\]])", r'<a href="\1">\1</a>', out)
    return out


def is_item(line):
    return line[:2] in ("- ", "* ", BULLET + " ")


def body_html(body):
    parts = []
    for block in re.split(r"\n\s*\n", body):
        lines = [l.rstrip() for l in block.strip().splitlines() if l.strip()]
        if not lines:
            continue
        if all(is_item(l) for l in lines):
            items = "".join(f"<li>{inline(l[2:].strip())}</li>" for l in lines)
            parts.append(f"<ul>{items}</ul>")
        else:
            parts.append("<p>" + "<br>".join(inline(l) for l in lines) + "</p>")
    return "\n".join(parts)


def nice_date(d):
    return f"{d.day} {d.strftime('%B %Y')}"


HEAD = """<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | Martin Jackson, Uncommon Sense</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#1A1A1A">
<meta property="og:type" content="{ogtype}">
<meta property="og:site_name" content="Uncommon Sense">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{image}">
<meta property="og:locale" content="en_GB">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Josefin+Sans:wght@300;400;600;700&family=Quicksand:wght@400;500;600&display=swap">
<link rel="stylesheet" href="/styles.css">
<script type="application/ld+json">
{jsonld}
</script>
</head>
<body>

<header class="site-header">
  <nav class="wrap nav" aria-label="Main">
    <a href="/"><img src="/assets/logo.svg" alt="Uncommon Sense home" width="130" height="56"></a>
    <ul>
      <li><a href="/#services">Services</a></li>
      <li><a href="/#approach">Approach</a></li>
      <li><a href="/#faq">FAQ</a></li>
      <li><a href="/writing/">Writing</a></li>
      <li><a class="btn btn-blue" href="{calendly}">Book a 30-minute call</a></li>
    </ul>
  </nav>
</header>

<main>
"""

FOOT = """
<section class="section contact" aria-labelledby="contact-h">
  <div class="wrap">
    <div class="contact-copy">
      <h2 id="contact-h">Have a decision that needs a second pair of eyes?</h2>
      <p>Thirty minutes, no pitch. You leave with a clearer next step either way.</p>
    </div>
    <div class="contact-actions">
      <a class="btn btn-dark" href="{calendly}">Book a 30-minute call</a>
      <a href="mailto:martin@uncommonsense-uk.com">martin@uncommonsense-uk.com</a>
    </div>
  </div>
</section>

</main>

<footer class="site-footer">
  <div class="wrap">
    <img src="/assets/logo-white.svg" alt="Uncommon Sense" width="121" height="52">
    <p>Uncommon Sense Consulting Limited · Registered in England and Wales, company number 06878365 · <a href="https://www.linkedin.com/in/uncommonsense">LinkedIn</a></p>
  </div>
</footer>

</body>
</html>
"""


def page(title, desc, url, image, jsonld, ogtype, content):
    head = HEAD.format(
        title=html.escape(title), desc=html.escape(desc), url=url, image=image,
        jsonld=json.dumps(jsonld, indent=2, ensure_ascii=False), ogtype=ogtype, calendly=CALENDLY,
    )
    return head + content + FOOT.format(calendly=CALENDLY)


def image_url(p):
    return f"{SITE}/assets/writing/{p['image']}" if p.get("image") else f"{SITE}/assets/og.jpg"


def article(p):
    url = f"{SITE}/writing/{p['slug']}/"
    jsonld = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": p["title"],
        "description": p["description"],
        "datePublished": p["date"],
        "url": url,
        "mainEntityOfPage": url,
        "image": image_url(p),
        "inLanguage": "en-GB",
        "author": {"@type": "Person", "@id": f"{SITE}/#martin", "name": "Martin Jackson", "url": f"{SITE}/"},
        "publisher": {"@id": f"{SITE}/#business"},
        "keywords": p["tag"],
    }
    if p.get("linkedin"):
        jsonld["sameAs"] = p["linkedin"]
    fig = ""
    if p.get("image"):
        fig = (f'<figure class="article-hero"><img src="/assets/writing/{p["image"]}" '
               f'alt="{html.escape(p["alt"])}"></figure>\n    ')
    origin = f'First published on LinkedIn on {nice_date(p["d"])}.'
    if p.get("linkedin"):
        origin = (f'First published on <a href="{p["linkedin"]}">LinkedIn</a> on {nice_date(p["d"])}. '
                  "The conversation is in the comments there.")
    content = f"""
<article class="section white article">
  <div class="wrap article-wrap">
    <p class="eyebrow"><a href="/writing/">Writing</a> · {html.escape(p['tag'])}</p>
    <h1>{html.escape(p['title'])}</h1>
    <p class="byline">Martin Jackson · <time datetime="{p['date']}">{nice_date(p['d'])}</time></p>
    {fig}<div class="article-body">
{body_html(p['body'])}
    </div>
    <p class="origin">{origin}</p>
  </div>
</article>
"""
    return page(p["title"], p["description"], url, image_url(p), jsonld, "article", content)


def card(p):
    return (f'<a class="post" href="/writing/{p["slug"]}/"><span class="tag">{html.escape(p["tag"])}</span>'
            f'<span class="title">{html.escape(p["title"])}</span></a>')


def index_page(posts):
    url = f"{SITE}/writing/"
    jsonld = {
        "@context": "https://schema.org",
        "@type": "Blog",
        "name": "Writing by Martin Jackson",
        "url": url,
        "author": {"@id": f"{SITE}/#martin"},
        "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": f"{SITE}/writing/{p['slug']}/",
                      "datePublished": p["date"]} for p in posts],
    }
    items = "\n".join(
        f'      <li><a href="/writing/{p["slug"]}/">{html.escape(p["title"])}</a>'
        f'<span>{html.escape(p["tag"])} · {nice_date(p["d"])}</span>'
        f'<p>{html.escape(p["description"])}</p></li>' for p in posts)
    content = f"""
<section class="section white">
  <div class="wrap article-wrap">
    <p class="eyebrow">Writing</p>
    <h1>Notes on technology, AI and the decisions around them</h1>
    <p class="lead">The posts readers responded to most, kept here so they stay findable. New writing goes out on <a href="https://www.linkedin.com/in/uncommonsense">LinkedIn</a> first.</p>
    <ul class="writing-list">
{items}
    </ul>
  </div>
</section>
"""
    desc = "Writing by Martin Jackson on technology strategy, AI governance and assurance, and the decisions boards and founders make about them."
    return page("Writing", desc, url, f"{SITE}/assets/og.jpg", jsonld, "website", content)


def replace_between(text, start, end, new):
    pat = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    if not pat.search(text):
        raise SystemExit(f"marker {start} not found")
    return pat.sub(lambda _: f"{start}\n{new}\n{end}", text)


def main():
    posts = sorted((parse(f) for f in (ROOT / "posts").glob("*.md")), key=lambda p: p["d"], reverse=True)
    out = ROOT / "writing"
    out.mkdir(exist_ok=True)
    keep = {p["slug"] for p in posts}
    for d in [d for d in out.iterdir() if d.is_dir()]:
        if d.name not in keep:
            for f in d.iterdir():
                f.unlink()
            d.rmdir()
    for p in posts:
        target = out / p["slug"]
        target.mkdir(parents=True, exist_ok=True)
        (target / "index.html").write_text(article(p), encoding="utf-8")
    (out / "index.html").write_text(index_page(posts), encoding="utf-8")

    home = ROOT / "index.html"
    cards = "\n".join(f"      {card(p)}" for p in posts[:3])
    home.write_text(replace_between(home.read_text(encoding="utf-8"),
                                    "<!-- writing:start -->", "<!-- writing:end -->", cards), encoding="utf-8")

    today = date.today().isoformat()
    urls = [(f"{SITE}/", today), (f"{SITE}/writing/", today)] + [
        (f"{SITE}/writing/{p['slug']}/", p["date"]) for p in posts]
    sm = "\n".join(f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{m}</lastmod>\n  </url>" for u, m in urls)
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + sm + "\n</urlset>\n", encoding="utf-8")

    llms = ROOT / "llms.txt"
    lines = "\n".join(f"- [{p['title']}]({SITE}/writing/{p['slug']}/): {p['description']}" for p in posts)
    llms.write_text(replace_between(llms.read_text(encoding="utf-8"),
                                    "<!-- writing:start -->", "<!-- writing:end -->", lines), encoding="utf-8")
    print(f"built {len(posts)} posts")


if __name__ == "__main__":
    main()
