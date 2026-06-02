@app.route("/api/dashboard")
def dashboard():

    try:

        data = {
            "summary": "INDSTAAL PEB Intelligence Live",
            "alerts": fetch_category_news("alerts"),
            "top_opportunities": fetch_category_news("opportunities"),
            "opportunities": fetch_category_news("opportunities"),
            "competitors": fetch_category_news("competitors"),
            "steel": fetch_category_news("steel"),
            "infra": fetch_category_news("infra")
        }

        return jsonify(data)

    except Exception as e:
        print("DASHBOARD ERROR:", e)

        return jsonify({
            "summary": "Fallback Mode Active",
            "alerts": [],
            "top_opportunities": [],
            "opportunities": [],
            "competitors": [],
            "steel": [],
            "infra": []
        })
