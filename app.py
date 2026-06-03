from flask import Flask, render_template, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return "PEB Dashboard Running Successfully"


@app.route("/api/dashboard")
def dashboard():

    return jsonify({
        "status": "ok",
        "message": "server running"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
