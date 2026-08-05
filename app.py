from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import time

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

        response = requests.get(url, timeout=10)

        end = time.time()

        response_time = round((end - start) * 1000, 2)

        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string.strip() if soup.title else "No Title"

        meta = soup.find("meta", attrs={"name": "description"})

        meta_description = (
            meta["content"]
            if meta and meta.get("content")
            else "No Meta Description"
        )

        h1_count = len(soup.find_all("h1"))

        images = soup.find_all("img")

        missing_alt = 0

        for img in images:
            if not img.get("alt"):
                missing_alt += 1

        text = soup.get_text()

        word_count = len(text.split())

        return jsonify({
            "status": response.status_code,
            "response_time": f"{response_time} ms",
            "title": title,
            "meta_description": meta_description,
            "h1_count": h1_count,
            "images_without_alt": missing_alt,
            "word_count": word_count
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)