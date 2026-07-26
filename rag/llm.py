import os

from groq import Groq

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def ask_llm(question, context):

    prompt = f"""
You are an enterprise customer support assistant.

You may receive:

COMPANY KNOWLEDGE

WEB KNOWLEDGE

Always prioritize COMPANY KNOWLEDGE.

Use WEB KNOWLEDGE only when company knowledge is incomplete.

If there is a conflict,

trust COMPANY KNOWLEDGE.

Never invent information.

Context:

{context}

Question:

{question}
"""

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )

    return response.choices[0].message.content