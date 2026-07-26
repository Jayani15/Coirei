import os
from app.repo_handler import clone_repo


def tool_clone_repo(repo_url):
    path = clone_repo(repo_url)
    return path


def tool_list_files(repo_path):

    python_files = []

    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.relpath(os.path.join(root, file), repo_path))

    return "\n".join(python_files[:15])


def tool_read_file(file_path):

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()[:4000]
    except:
        return "Error reading file"


TOOLS = {
    "clone_repo": tool_clone_repo,
    "list_files": tool_list_files,
    "read_file": tool_read_file,
}