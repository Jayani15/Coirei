from sentence_transformers import SentenceTransformer, util
import torch
import json
from datetime import datetime
import re

# Load FAQ data
with open("faq.json") as f:
    faqs = json.load(f)

model = SentenceTransformer('all-MiniLM-L6-v2')

questions = [faq["question"] for faq in faqs]
question_embeddings = model.encode(questions, convert_to_tensor=True)

# -------- Intent Detection --------
def detect_intent(query):
    q = query.lower()

    if any(word in q for word in ["refund", "money back"]):
        return "refund"
    elif any(word in q for word in ["password", "login"]):
        return "password"
    elif any(word in q for word in ["agent", "human", "support"]):
        return "escalate"
    return "unknown"

# -------- FAQ Retrieval --------
def clean_text(text):
    return re.sub(r"[^\w\s]", "", text.lower())

def get_answer(query):
    query_embedding = model.encode(query, convert_to_tensor=True)

    scores = util.cos_sim(query_embedding, question_embeddings)
    best_idx = torch.argmax(scores)

    best_score = scores[0][best_idx].item()

    if best_score > 0.5:
        return faqs[best_idx]["answer"]

    return None

# -------- Escalation Logic --------
def should_escalate(intent, answer):
    if intent == "escalate":
        return True
    if intent == "unknown" and answer is None:
        return True
    return False

# -------- Logging --------
def log_chat(user, bot):
    with open("logs.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} | User: {user} | Bot: {bot}\n")

# -------- Chat Interface --------
def chat():
    print("🤖 Customer Support Agent (type 'exit' to quit)\n")

    while True:
        user = input("You: ")
        if user.lower() == "exit":
            print("Goodbye!")
            break

        intent = detect_intent(user)
        answer = get_answer(user)

        if should_escalate(intent, answer):
            bot = "⚠️ Your issue has been escalated to a human agent."
        elif answer:
            bot = answer
        else:
            bot = "I didn't understand that. Can you rephrase?"

        print("Bot:", bot)
        log_chat(user, bot)

if __name__ == "__main__":
    chat()