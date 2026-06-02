from flask import Flask, render_template, jsonify
from flask_cors import CORS

# ---------------- CREATE APP FIRST ----------------
app = Flask(__name__)
CORS(app)


# ---------------- HOME PAGE ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- API ----------------
@app.route("/api/dashboard")
def dashboard():

    return jsonify({
        "summary": "INDSTAAL Dashboard LIVE (Stable Version)",

        "alerts": [
            {
                "title": "System Working Successfully",
                "link": "#",
                "insight": "Backend is now stable",
                "impact": "HIGH",
                "tag": "SYSTEM",
                "score": 100,
                "date": "NOW"
            }
        ],

        "top_opportunities": [],
        "opportunities": [],
        "competitors": [],
        "steel": [],
        "infra": []
    })


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
