import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
print("Loaded NEWS_API_KEY:", NEWS_API_KEY)
NEWS_URL = "https://newsapi.org/v2/top-headlines?country=us&pageSize=5"

MODEL_NAME = "llama-3.1-8b-instant"