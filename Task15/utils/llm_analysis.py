import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_report(report):
    prompt = f"""
    You are a QA testing expert.

    Analyze this website test report:
    {report}

    Identify:
    - UI issues
    - Functional bugs
    - Severity (Low, Medium, High)

    Give structured output.
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content