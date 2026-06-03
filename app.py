from flask import Flask, render_template, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return "PEB Dashboard Running Successfully"


from intelligence import fetch_category_news


@app.route("/api/dashboard")
def dashboard():

    return jsonify({
        "summary": "INDSTAAL Intelligence Live",

        "alerts": fetch_category_news("alerts"),
        "top_opportunities": fetch_category_news("opportunities"),
        "opportunities": fetch_category_news("opportunities"),
        "competitors": fetch_category_news("competitors"),
        "steel": fetch_category_news("steel"),
        "infra": fetch_category_news("infra")
    })
