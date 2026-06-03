import feedparser
import urllib.parse

# ----------------------------
# YOUR KEYWORDS STRUCTURE
# ----------------------------
from keywords import (
    competitors,
    clients,
    steel_keywords,
    demand_keywords,
    infra_keywords
)


# ----------------------------
# MAP KEYWORDS TO CATEGORIES
# ----------------------------
queries = {
    "competitors": competitors,
    "alerts": clients,
    "steel": steel_keywords,
    "opportunities": demand_keywords,
    "infra": infra_keywords
}


# ----------------------------
# STORY FILTER (REMOVE DUPLICATES)
# ----------------------------
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


# ----------------------------
# MAIN NEWS FUNCTION
# ----------------------------
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

                    # ---------------- DUPLICATE CHECK ----------------
                    if link in seen_links:
                        continue

                    key = story_key(title)

                    if key in seen_stories:
                        continue

                    seen_links.add(link)
                    seen_stories.add(key)

                    # ---------------- FINAL OUTPUT ----------------
                    results.append({
                        "title": title,
                        "link": link,
                        "date": getattr(entry, "published", "Recent"),
                        "insight": "AI detected relevant industry movement",
                        "impact": "MEDIUM",
                        "tag": category.upper(),
                        "score": len(title)
                    })

                except Exception as e:
                    print("ENTRY ERROR:", e)
                    continue

        except Exception as e:
            print("RSS ERROR:", e)
            continue

    # sort by relevance
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return results[:10]
