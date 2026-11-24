"""Pull the newest Substack posts into posts.json for the website."""
import json
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

FEED = "https://devinpavlou.substack.com/feed"
MONTHS = ["Jan.", "Feb.", "March", "April", "May", "June", "July",
          "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]

req = urllib.request.Request(FEED, headers={"User-Agent": "devinpavlou.com posts updater"})
with urllib.request.urlopen(req, timeout=30) as r:
    root = ET.fromstring(r.read())

posts = []
for item in root.iter("item"):
    d = parsedate_to_datetime(item.findtext("pubDate"))
    posts.append({
        "title": item.findtext("title", "").strip(),
        "url": item.findtext("link", "").strip(),
        "date": f"{MONTHS[d.month - 1]} {d.day}, {d.year}",
    })
    if len(posts) == 3:
        break

with open("posts.json", "w") as f:
    json.dump(posts, f, indent=2)
print(f"Wrote {len(posts)} posts")
