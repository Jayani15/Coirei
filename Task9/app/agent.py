from app.llm import ask_llm
from app.tools import TOOLS


SYSTEM_PROMPT = """
You are an AI code review agent.

You must analyze the repository using the tools before producing the final answer.

Rules:
- First clone the repository
- Then inspect Python files
- Read at least 3 important Python files
- Only after analyzing files produce FINAL_ANSWER

Available tools:
1. clone_repo(repo_url)
2. list_files(repo_path)
3. read_file(file_path)

Tool usage format:

ACTION: tool_name
INPUT: argument

When finished, produce the final report EXACTLY in this format:

FINAL_ANSWER:

PROJECT_SUMMARY:
<what the project does>

CODE_QUALITY_ISSUES:
<list of problems in the code>

SUGGESTED_IMPROVEMENTS:
<how to improve the code>

CONFIDENCE_SCORE:
<number between 0 and 1>
"""

def parse_action(text):

    lines = text.split("\n")

    action = None
    input_arg = None

    for line in lines:
        if line.startswith("ACTION:"):
            action = line.replace("ACTION:", "").strip()

        if line.startswith("INPUT:"):
            input_arg = line.replace("INPUT:", "").strip()

    return action, input_arg


def run_agent(repo_url):

    context = f"{SYSTEM_PROMPT}\n\nUser request: Review this repo {repo_url}"

    for _ in range(15):  # limit steps

        response = ask_llm(context)
        print("\nLLM RESPONSE:\n", response)

        if "FINAL_ANSWER:" in response:
            return response.split("FINAL_ANSWER:")[1].strip()

        action, arg = parse_action(response)

        if action in TOOLS:

            result = TOOLS[action](arg)
            print("\nTOOL RESULT:\n", result)

            context += f"\nLLM: {response}\nObservation: {result}"

        else:
            return "Agent failed to choose a valid tool."

    return "Agent stopped after too many steps."