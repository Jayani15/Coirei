import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def evaluate_context(results):
    """
    Classifies retrieval results based on Qdrant similarity scores.

    Rules:
    Correct   : At least one chunk has score > 0.75
    Incorrect : All chunks have score <= 0.3
    Ambiguous : Otherwise
    """

    scores = [r.score for r in results]

    if any(score > 0.75 for score in scores):
        status = "Correct"

    elif all(score <= 0.3 for score in scores):
        status = "Incorrect"

    else:
        status = "Ambiguous"

    return {
        "status": status,
        "scores": scores
    }


def refine_context(question, context):
    """
    Removes irrelevant information from retrieved chunks.
    Used only for Ambiguous retrieval.
    """

    prompt = f"""
You are a Knowledge Refinement system.

Question:
{question}

Retrieved Context:
{context}

Instructions:

- Remove all irrelevant information.
- Keep only the information useful for answering the question.
- Do not summarize.
- Do not add new information.
- Preserve the original wording as much as possible.

Return ONLY the refined context.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content.strip()
