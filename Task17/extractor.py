import os
import json
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_resume_data(resume_text):
    prompt = f"""
Extract the following details from the resume.

Return ONLY valid JSON:
{{
  "name": "string",
  "skills": ["skill1", "skill2"],
  "experience": number,
  "education": "string"
}}

DO NOT return nested objects for experience.

Resume:
{resume_text[:4000]}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    content = response.choices[0].message.content

    try:
        data = json.loads(content)
    except:
        start = content.find("{")
        end = content.rfind("}") + 1
        data = json.loads(content[start:end])

    return data