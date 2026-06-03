import feedparser
import urllib.parse
from keywords import (
    competitors,
    clients,
    steel_keywords,
    demand_keywords,
    infra_keywords
)

# ---------------- CATEGORY MAP ----------------
queries = {
    "competitors": competitors,
    "alerts": clients,
    "steel": steel_keywords,
    "opportunities": demand_keywords,
    "infra": infra_keywords
}


# ---------------- REMOVE DUPLICATES ----------------
def story_key(title):
    title = title.lower()

    remove_words = [
        "india", "project", "projects",
        "new", "latest", "update",
        "contract", "order", "expansion"
    ]

    for w in remove_words:
        title = title.replace(w, "")

    return " ".join(title.split()[:5])


# ---------------- MAIN FUNCTION ----------------
def fetch_category_news(category):

    results = []
    seen_links = set()
    seen_stories = set()

    search_list = queries.get(category, [])

    if not search_list:
        return []

    for q in search_list:

        try:
            url = (
                "https://news.google.com/rss/search?q="
                + urllib.parse.quote(q)
                + "&hl=en-IN&gl=IN&ceid=IN:en"
            )

            feed = feedparser.parse(url)

            for entry in feed.entries:

                try:
                    title = entry.title
                    link = entry.link

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
                        "insight": "AI detected industry movement",
                        "impact": "MEDIUM",
                        "tag": category.upper(),
                        "score": len(title)
                    })

                except:
                    continue

        except:
            continue

    return sorted(results, key=lambda x: x["score"], reverse=True)[:10]
