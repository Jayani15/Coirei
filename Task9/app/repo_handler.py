import os
import shutil
from git import Repo

TEMP_DIR = "temp_repos"

def clone_repo(repo_url: str) -> str:
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    repo_name = repo_url.split("/")[-1].replace(".git", "")
    local_path = os.path.join(TEMP_DIR, repo_name)

    # Remove if already exists
    if os.path.exists(local_path):
        shutil.rmtree(local_path)

    Repo.clone_from(repo_url, local_path)
    return local_path