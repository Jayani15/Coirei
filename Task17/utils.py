import os

def load_resumes(folder_path):
    files = []
    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            files.append(os.path.join(folder_path, file))
    return files


def load_jd(file_path):
    with open(file_path, "r") as f:
        return f.read()