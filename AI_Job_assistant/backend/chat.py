import os
from dotenv import load_dotenv
from openai import OpenAI
from rag import search_job_description

from memory import (
    get_conversation,
    save_message,
    get_user_memory,
    save_user_memory
)

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def chat_with_ai(message: str, user_id: int, job_id: str = None):

    history = get_conversation(user_id)

    user_memory = get_user_memory(user_id)

    save_message(
        user_id,
        "user",
        message
    )

    history = get_conversation(user_id)

    memory_context = ""

    if user_memory:
        memory_context = (
            "Known information about the user:\n"
            + "\n".join(
                f"{key}: {value}"
                for key, value in user_memory.items()
            )
        )

    jd_context = ""

    if job_id:
        retrieved_chunks = search_job_description(
            message,
            job_id
        )

        jd_context = (
            "Relevant information from the job description:\n"
            + "\n".join(retrieved_chunks)
        )

    system_prompt = """
You are an AI Career Assistant.

Use the user's stored information when relevant.

If job-description information is provided, use it
to answer questions about the job.

Do not invent requirements that are not present
in the provided job description.
"""

    if memory_context:
        system_prompt += "\n\n" + memory_context

    if jd_context:
        system_prompt += "\n\n" + jd_context

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    messages.extend(history)

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages
    )

    answer = response.choices[0].message.content

    save_message(
        user_id,
        "assistant",
        answer
    )

    return answer

def extract_user_memory(message: str):

    message_lower = message.lower()

    memories = []

    if "i want to become" in message_lower:

        value = message.split(
            "I want to become",
            1
        )[1].strip()

        memories.append(
            ("career_goal", value)
        )

    if "i prefer" in message_lower:

        value = message.split(
            "I prefer",
            1
        )[1].strip()

        memories.append(
            ("preference", value)
        )

    return memories