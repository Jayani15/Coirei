SYSTEM_PROMPT = """
You are an AI Career Assistant.

You help candidates with:
- Job descriptions
- Career guidance
- Interview preparation
- Technical questions
- Learning recommendations

Use the provided memory and job information
when answering the user.
"""


def build_prompt(message, memory, job_context=""):

    conversation = memory.get("conversation", [])
    user_info = memory.get("user", {})

    prompt = f"""
{SYSTEM_PROMPT}

USER MEMORY:
{user_info}

CONVERSATION HISTORY:
{conversation}

JOB DESCRIPTION CONTEXT:
{job_context}

CURRENT QUESTION:
{message}

Provide a helpful, accurate and conversational response.
"""

    return prompt