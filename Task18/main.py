from groq import Groq
from config import GROQ_API_KEY, MODEL_NAME
from utils import fetch_news, extract_text, save_output
from prompts import SUMMARIZE_PROMPT, CATEGORY_PROMPT

client = Groq(api_key=GROQ_API_KEY)


# ------------------------
# LLM: Summarization
# ------------------------
def summarize(text):
    prompt = SUMMARIZE_PROMPT.format(text=text[:3000])

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )

    return response.choices[0].message.content.strip()


# ------------------------
# LLM: Categorization
# ------------------------
def categorize(summary):
    prompt = CATEGORY_PROMPT.format(text=summary)

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    return response.choices[0].message.content.strip()


# ------------------------
# Main Pipeline
# ------------------------
def main():
    print("Fetching news...")
    articles = fetch_news()

    results = []

    for article in articles:
        print(f"Processing: {article['title']}")

        content = extract_text(article["url"])

        if not content:
            continue

        summary = summarize(content)
        category = categorize(summary)

        results.append({
            "title": article["title"],
            "summary": summary,
            "category": category
        })

    save_output(results)
    print("Done! Saved to output.json")


if __name__ == "__main__":
    main()