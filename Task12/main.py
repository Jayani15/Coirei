import os
import subprocess
import requests
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage


# =========================
# CONFIG
# =========================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

WORKSPACE = "workspace"
os.makedirs(WORKSPACE, exist_ok=True)

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.1-8b-instant"
)


# =========================
# TOOL: Clone Repo
# =========================

def clone_repo(repo_url):
    name = repo_url.split("/")[-1].replace(".git", "")
    path = os.path.join(WORKSPACE, name)

    if not os.path.exists(path):
        subprocess.run(["git", "clone", repo_url, path])

    return path


# =========================
# TOOL: Linter
# =========================

def run_linter(path):
    result = subprocess.run(
        ["flake8", path],
        capture_output=True,
        text=True
    )

    return result.stdout[:2000]


# =========================
# TOOL: Security Scan
# =========================

def run_security(path):
    result = subprocess.run(
        ["bandit", "-r", path],
        capture_output=True,
        text=True
    )

    return result.stdout[:2000]


# =========================
# TOOL: Run Tests
# =========================

def run_tests(path):
    result = subprocess.run(
        ["pytest", path],
        capture_output=True,
        text=True
    )

    return result.stdout[:2000]


# =========================
# TOOL: Git Branch
# =========================

def create_branch(path):

    subprocess.run(
        ["git", "-C", path, "checkout", "-b", "ai-fixes"],
        capture_output=True
    )


# =========================
# TOOL: Commit
# =========================

def commit_changes(path):

    subprocess.run(["git", "-C", path, "add", "."])
    subprocess.run(
        ["git", "-C", path, "commit", "-m", "AI DevOps fixes"]
    )


# =========================
# TOOL: Push Branch
# =========================

def push_branch(path):

    subprocess.run(
        ["git", "-C", path, "push", "origin", "ai-fixes"]
    )


# =========================
# TOOL: Create PR
# =========================

def create_pr(repo_url):

    if not GITHUB_TOKEN:
        print("No GitHub token found. Skipping PR creation.")
        return

    repo = repo_url.replace("https://github.com/", "").replace(".git", "")

    url = f"https://api.github.com/repos/{repo}/pulls"

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    data = {
        "title": "AI DevOps Agent Fixes",
        "body": "Automated fixes suggested by AI DevOps Agent",
        "head": "ai-fixes",
        "base": "main"
    }

    response = requests.post(url, headers=headers, json=data)

    print("PR Response:", response.json())


# =========================
# AGENT ANALYSIS
# =========================

def analyze(lint, security, tests):

    prompt = f"""
You are an AI DevOps Engineer.

Analyze the repository reports.

LINT REPORT:
{lint}

SECURITY REPORT:
{security}

TEST REPORT:
{tests}

Provide:
1. Major issues
2. Security problems
3. Suggested fixes
4. Code improvements
"""

    response = llm.invoke(
        [HumanMessage(content=prompt)]
    )

    return response.content


# =========================
# MAIN WORKFLOW
# =========================

def main():

    repo_url = input("Enter GitHub Repo URL: ")

    print("\nCloning repository...")
    path = clone_repo(repo_url)

    print("Running linter...")
    lint = run_linter(path)

    print("Running security scan...")
    security = run_security(path)

    print("Running tests...")
    tests = run_tests(path)

    print("Analyzing with AI...\n")

    report = analyze(lint, security, tests)

    print("===== AI REPORT =====\n")
    print(report)

    print("\nCreating branch...")
    create_branch(path)

    print("Committing changes...")
    commit_changes(path)

    print("Pushing branch...")
    push_branch(path)

    print("Creating Pull Request...")
    create_pr(repo_url)

    print("\nAgent finished.")


# =========================

if __name__ == "__main__":
    main()