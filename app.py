from flask import Flask, render_template, jsonify
from flask_cors import CORS

from intelligence import fetch_category_news

app = Flask(__name__)
CORS(app)

# ----------------------------
# HOME PAGE (IMPORTANT)
# ----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# ----------------------------
# DASHBOARD API
# ----------------------------
@app.route("/api/dashboard")
def dashboard():

    data = {
        "summary": "PEB Intelligence Dashboard Active",
        "alerts": fetch_category_news("alerts"),
        "top_opportunities": fetch_category_news("opportunities"),
        "opportunities": fetch_category_news("opportunities"),
        "competitors": fetch_category_news("competitors"),
        "steel": fetch_category_news("steel"),
        "infra": fetch_category_news("infra")
    }

    return jsonify(data)


# ----------------------------
# MAIN RUN (LOCAL ONLY)
# ----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
