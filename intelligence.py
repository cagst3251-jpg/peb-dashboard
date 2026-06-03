import socket
socket.setdefaulttimeout(10)

import feedparser
import urllib.parse
from datetime import datetime, timedelta


def is_recent(entry):
    try:
        if not hasattr(entry, "published_parsed"):
            return True

        published = datetime(*entry.published_parsed[:6])
        return published >= datetime.now() - timedelta(days=7)
    except:
        return True


def story_key(title):
    title = title.lower()

    remove_words = [
        "india",
        "project",
        "projects",
        "new",
        "latest",
        "update",
        "expansion",
        "contract",
        "order"
    ]

    for word in remove_words:
        title = title.replace(word, "")

    return " ".join(title.split()[:5])


def score(title):
    t = title.lower()
    s = 10

    keywords = [
        "adani",
        "l&t",
        "tata",
        "jsw",
        "steel",
        "warehouse",
        "data center",
        "factory",
        "contract",
        "tender",
        "order"
    ]

    for k in keywords:
        if k in t:
            s += 10

    return min(s, 100)


def category_tag(title):
    t = title.lower()

    if "steel" in t:
        return "🔵 STEEL"

    if "adani" in t or "l&t" in t:
        return "🟢 CLIENT"

    if "interarch" in t or "kirby" in t:
        return "🔴 COMPETITOR"

    return "⚪ GENERAL"


def generate_insight(title):
    t = title.lower()

    if "warehouse" in t:
        return "Warehouse opportunity"

    if "data center" in t:
        return "High-value infra opportunity"

    if "steel" in t:
        return "Steel market movement"

    return "Industry update"


queries = {
    "opportunities": [
        "warehouse project India",
        "data center India",
        "industrial project India",
        "factory expansion India"
    ],
    "competitors": [
        "Interarch project India",
        "Kirby Building Systems India",
        "PEB company India"
    ],
    "steel": [
        "steel price India",
        "HRC steel India"
    ],
    "infra": [
        "industrial corridor India",
        "infrastructure India"
    ]
}


def fetch_category_news(category):

    results = []

    seen_links = set()
    seen_stories = set()

    search_list = queries.get(category, [])

    for q in search_list:

        try:
            query = urllib.parse.quote(q)

            url = (
                "https://news.google.com/rss/search?q="
                + query +
                "&hl=en-IN&gl=IN&ceid=IN:en"
            )

            feed = feedparser.parse(url)

            for entry in feed.entries:

                try:
                    if not is_recent(entry):
                        continue

                    title = entry.title.strip().lower()
                    link = entry.link

                    story = story_key(title)

                    if story in seen_stories:
                        continue
                    seen_stories.add(story)

                    if link in seen_links:
                        continue
                    seen_links.add(link)

                    results.append({
                        "title": entry.title,
                        "link": entry.link,
                        "date": getattr(entry, "published", "Recent"),
                        "insight": generate_insight(entry.title),
                        "impact": "HIGH" if score(entry.title) > 60 else "MEDIUM",
                        "tag": category_tag(entry.title),
                        "score": score(entry.title)
                    })

                except:
                    continue

        except Exception as e:
            print("RSS Error:", e)
            continue

    results.sort(key=lambda x: x["score"], reverse=True)

    return results[:10]