import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL_NAME = "llama-3.1-8b-instant"  

def call_llm(prompt: str) -> dict:
    """
    Calls Groq LLaMA model and returns structured JSON response.
    """

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a precise debugging assistant that strictly returns valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,  # low = more deterministic debugging
            response_format={"type": "json_object"}  # Forces JSON output
        )

        content = completion.choices[0].message.content

        # Parse JSON safely
        parsed = json.loads(content)

        return parsed

    except Exception as e:
        return {
            "explanation": f"LLM call failed: {str(e)}",
            "suggested_fix": "Check Groq API key or response formatting.",
            "corrected_code": "",
            "confidence": 0.0
        }