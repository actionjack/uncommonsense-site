#!/usr/bin/env python3
"""Tell IndexNow search engines (Bing, Yandex, Seznam, Naver) about every URL in sitemap.xml.
Run after a push has deployed: python3 indexnow.py. Standard library only."""
import json, re, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
KEY = "70c649c040ae10255b752e02bc3f45d9"
urls = re.findall(r"<loc>(.*?)</loc>", (ROOT / "sitemap.xml").read_text())
body = json.dumps({"host": "uncommonsense-uk.com", "key": KEY,
                   "keyLocation": f"https://uncommonsense-uk.com/{KEY}.txt", "urlList": urls}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                             headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req, timeout=30) as r:
    print(f"IndexNow {r.status}: {len(urls)} URLs submitted")
