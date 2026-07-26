import requests
import json
from newspaper import Article
from config import NEWS_API_KEY, NEWS_URL

# ------------------------
# Fetch News
# ------------------------
def fetch_news():
    url = f"{NEWS_URL}&apiKey={NEWS_API_KEY}"
    response = requests.get(url)

    print("Status Code:", response.status_code)
    print("Response:", response.text)   # 👈 ADD THIS

    if response.status_code != 200:
        raise Exception("Failed to fetch news")

    data = response.json()
    articles = data.get("articles", [])

    return [
        {"title": a["title"], "url": a["url"]}
        for a in articles if a.get("url")
    ]


# ------------------------
# Extract Article Text
# ------------------------
def extract_text(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception:
        return ""


# ------------------------
# Save Output
# ------------------------
def save_output(results, filename="output.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)