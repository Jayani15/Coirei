from app.prompt import SYSTEM_PROMPT
from app.llm import call_llm


def debug_agent(error_traceback: str, code_snippet: str):
    user_prompt = f"""
Error Traceback:
{error_traceback}

Code:
{code_snippet}
"""

    full_prompt = SYSTEM_PROMPT + "\n" + user_prompt

    response = call_llm(full_prompt)

    return response