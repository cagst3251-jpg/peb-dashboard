from flask import Flask, render_template, jsonify
from flask_cors import CORS

from intelligence import fetch_category_news

app = Flask(__name__)
CORS(app)


# -------------------------
# HOME PAGE
# -------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -------------------------
# DASHBOARD API
# -------------------------
@app.route("/api/dashboard")
def dashboard():

    return {
        "summary": "LIVE SYSTEM RUNNING",
        "alerts": [
            {
                "title": "System Test News Active",
                "link": "#",
                "insight": "Backend is working",
                "impact": "HIGH",
                "tag": "TEST",
                "score": 100,
                "date": "Now"
            }
        ],
        "top_opportunities": [],
        "opportunities": [],
        "competitors": [],
        "steel": [],
        "infra": []
    }
        return jsonify(data)

    except Exception as e:
        print("DASHBOARD ERROR:", e)

        return jsonify({
            "summary": "System Running (Fallback Mode)",
            "alerts": [],
            "top_opportunities": [],
            "opportunities": [],
            "competitors": [],
            "steel": [],
            "infra": []
        })


# -------------------------
# RUN LOCAL ONLY
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
