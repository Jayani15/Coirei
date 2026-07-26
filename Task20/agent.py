from groq import Groq
from prompts import SYSTEM_PROMPT
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def process_complaint(complaint_text):
    prompt = f"""
Customer Complaint:
{complaint_text}

Analyze this complaint and return ONLY valid JSON with:

{{
    "category": "",
    "sentiment": "",
    "urgency_level": "",
    "decision": "",
    "justification": "",
    "priority_score": 0
}}

Rules:
- category must be one of: Delivery, Payment, Service, Technical
- decision must be one of: Refund, Escalate, Resolve
- priority_score must be between 1 and 10
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    output = response.choices[0].message.content

    try:
        return json.loads(output)
    except:
        return {
            "error": "Invalid JSON returned by model",
            "raw_output": output
        }