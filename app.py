from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import time
import os

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    url = data.get("url", "").strip()

    if not url:
        return jsonify({"error": "Please enter a URL"}), 400

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    try:
        start = time.time()

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=10)

        end = time.time()

        response_time = round((end - start) * 1000, 2)

        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string.strip() if soup.title and soup.title.string else "No Title"

        meta = soup.find("meta", attrs={"name": "description"})
        if meta and meta.get("content"):
            description = meta["content"]
        else:
            description = "No Meta Description"

        h1_count = len(soup.find_all("h1"))

        images = soup.find_all("img")
        missing_alt = sum(1 for img in images if not img.get("alt"))

        words = len(soup.get_text().split())

        return jsonify({
            "status": response.status_code,
            "response_time": response_time,
            "title": title,
            "description": description,
            "h1_count": h1_count,
            "missing_alt": missing_alt,
            "word_count": words
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)