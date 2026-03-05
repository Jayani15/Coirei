# Python Code Sandboxing System

A secure Python execution sandbox that safely runs user-submitted Python code while preventing malicious actions such as OS command execution, file deletion, and network access.

---

# Objective

The goal of this project is to build a system that can:

- Run arbitrary Python code
- Prevent dangerous operations
- Enforce execution limits
- Return structured execution results

This type of system is commonly used in **online judges, coding platforms, and AI code interpreters**.

---

# Features

- Secure execution of Python code
- Prevention of OS command execution
- Prevention of file deletion
- Blocking of network calls
- Execution timeout protection
- Memory usage monitoring
- Structured JSON output

---

# Response Format

The system returns results in the following structure:

```json
{
  "status": "success/failure",
  "stdout": "",
  "stderr": "",
  "execution_time_ms": 0,
  "memory_usage_mb": 0
}
```

---

# Installation

Clone the repository:

```bash
git clone <repository_url>
cd code-sandbox
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Running the Server

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The server will run at:

```
http://127.0.0.1:8000
```

API documentation is available at:

```
http://127.0.0.1:8000/docs
```

---

# Example Request

```json
{
  "code": "print('Hello Sandbox')"
}
```

---

# Example Response

```json
{
  "status": "success",
  "stdout": "Hello Sandbox\n",
  "stderr": "",
  "execution_time_ms": 12,
  "memory_usage_mb": 3
}
```

---

# Security Protections

The sandbox blocks dangerous operations including:

- OS command execution (`os`, `subprocess`)
- File system manipulation (`os`, `shutil`)
- Network access (`socket`, `requests`)
- Dynamic code execution (`eval`, `exec`)

Security mechanisms used:

- Keyword filtering
- Subprocess isolation
- Execution timeout
- Memory usage monitoring

---

# Example Malicious Code

Example attack attempt:

```python
import os
os.system("rm -rf /")
```

Result: **Blocked**

Example infinite loop:

```python
while True:
    pass
```

Result: **Terminated due to timeout**

---

# Performance

Benchmark results are available in:

```
docs/benchmarks.md
```

Typical execution time for simple programs:

- 10–20 ms

Memory usage:

- 3–5 MB

---

# Future Improvements

Potential improvements for stronger sandboxing:

- Docker container isolation
- cgroups resource limits
- seccomp syscall filtering
- AST-based static code analysis
- restricted Python interpreter

---

# License

This project is licensed under the MIT License.