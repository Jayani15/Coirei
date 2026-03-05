from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import tempfile
import time
import psutil
import sys

app = FastAPI()

# keywords to block
FORBIDDEN = [
    "os",
    "sys",
    "subprocess",
    "socket",
    "shutil",
    "requests",
    "__import__",
    "eval",
    "exec",
    "open"
]


class CodeRequest(BaseModel):
    code: str


def validate_code(code):
    for word in FORBIDDEN:
        if word in code:
            raise ValueError(f"Forbidden keyword: {word}")


@app.post("/execute")
def execute(req: CodeRequest):

    try:
        validate_code(req.code)
    except Exception as e:
        return {
            "status": "failure",
            "stdout": "",
            "stderr": str(e),
            "execution_time_ms": 0,
            "memory_usage_mb": 0
        }

    start = time.time()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as f:
        f.write(req.code.encode())
        filename = f.name

    process = subprocess.Popen(
        [sys.executable, filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    try:
        stdout, stderr = process.communicate(timeout=2)
    except subprocess.TimeoutExpired:
        process.kill()
        return {
            "status": "failure",
            "stdout": "",
            "stderr": "Execution timeout",
            "execution_time_ms": 2000,
            "memory_usage_mb": 0
        }

    end = time.time()

    try:
        mem = psutil.Process(process.pid).memory_info().rss / (1024 * 1024)
    except:
        mem = 0

    return {
        "status": "success" if process.returncode == 0 else "failure",
        "stdout": stdout,
        "stderr": stderr,
        "execution_time_ms": int((end - start) * 1000),
        "memory_usage_mb": round(mem, 2)
    }