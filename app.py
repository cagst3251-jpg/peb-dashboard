from flask import Flask, render_template, jsonify

from intelligence import fetch_category_news

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# ALERT DETECTION
# -----------------------------

ALERT_CLIENTS = [
    "adani", "l&t", "tata", "jsw", "reliance", "vedanta", "birla"
]


def detect_alerts(news_list):
    alerts = []

    for item in news_list:
        title = item["title"].lower()

        for c in ALERT_CLIENTS:
            if c in title:
                alerts.append({
                    "title": item["title"],
                    "link": item["link"],
                    "tag": "🚨 CLIENT ALERT",
                    "impact": "CRITICAL"
                })
                break

    return alerts


# -----------------------------
# TOP OPPORTUNITIES FILTER
# -----------------------------

def top_opportunities(news_list):
    return [n for n in news_list if n["score"] >= 70][:5]


# -----------------------------
# SUMMARY ENGINE (IMPROVED)
# -----------------------------

def generate_summary(op, comp, steel, infra):

    parts = []

    if op:
        parts.append("High-value project opportunities detected.")

    if comp:
        parts.append("Competitor activity increasing in PEB sector.")

    if steel:
        parts.append("Steel price movement may impact project margins.")

    if infra:
        parts.append("Infrastructure pipeline remains active.")

    if not parts:
        return "Market is stable with low activity."

    return " ".join(parts)


# -----------------------------
# MAIN API
# -----------------------------

@app.route("/api/dashboard")
def dashboard():

    opportunities = fetch_category_news("opportunities")
    competitors = fetch_category_news("competitors")
    steel = fetch_category_news("steel")
    infra = fetch_category_news("infra")

    alerts = detect_alerts(
        opportunities + competitors + steel + infra
    )

    top_ops = top_opportunities(opportunities)

    summary = generate_summary(opportunities, competitors, steel, infra)

    return jsonify({
        "summary": summary,
        "alerts": alerts,
        "top_opportunities": top_ops,
        "opportunities": opportunities,
        "competitors": competitors,
        "steel": steel,
        "infra": infra
    })


if __name__ == "__main__":
    app.run(debug=True)