import feedparser
import urllib.parse
import time


# -------------------------
# KEYWORDS
# -------------------------
queries = {
    "alerts": [
        "PEB steel plant India news",
        "industrial accident factory India",
        "major infrastructure delay India"
    ],
    "opportunities": [
        "new warehouse construction India",
        "industrial project order India PEB",
        "factory expansion contract India"
    ],
    "competitors": [
        "Kirby building systems order",
        "Interarch projects India",
        "Zamil steel India contract"
    ],
    "steel": [
        "steel price India HRC",
        "steel market India update",
        "Tata steel price trend"
    ],
    "infra": [
        "infrastructure project India bridge highway",
        "industrial park development India",
        "logistics warehouse India project"
    ]
}


# -------------------------
# SIMPLE STORY FILTER
# -------------------------
def story_key(title):
    title = title.lower()

    remove_words = [
        "india", "project", "projects", "latest",
        "new", "update", "expansion", "contract"
    ]

    for w in remove_words:
        title = title.replace(w, "")

    return " ".join(title.split()[:5])


# -------------------------
# RSS NEWS FETCH
# -------------------------
def fetch_category_news(category):

    results = []

    seen_links = set()
    seen_stories = set()

    search_list = queries.get(category, [])

    if not search_list:
        return []

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
                    title = entry.title.strip()
                    link = entry.link

                    # skip duplicates
                    if link in seen_links:
                        continue

                    key = story_key(title)

                    if key in seen_stories:
                        continue

                    seen_links.add(link)
                    seen_stories.add(key)

                    results.append({
                        "title": title,
                        "link": link,
                        "date": getattr(entry, "published", "Recent"),
                        "insight": "AI detected relevant business update",
                        "impact": "MEDIUM",
                        "tag": category.upper(),
                        "score": len(title) + len(link)
                    })

                except:
                    continue

        except Exception as e:
            print("RSS ERROR:", e)
            continue

    # sort + limit
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return results[:10]
