# Code Sandboxing System – Architecture

## Overview

This system provides a secure environment to execute arbitrary Python code while preventing harmful operations such as:

- File deletion
- OS command execution
- Network calls
- Infinite loops
- Resource abuse

The sandbox uses **FastAPI**, **subprocess isolation**, and **runtime monitoring** to safely execute user code.

---

## Architecture Flow

User → FastAPI API → Code Validator → Python Subprocess Sandbox → Result Formatter → JSON Response

---

## Components

### 1. FastAPI Server
Handles incoming requests containing Python code.

Responsibilities:
- Accept user code
- Validate request structure
- Send code to sandbox executor
- Return execution results

---

### 2. Code Validation Layer

Before execution, the code is scanned for dangerous keywords such as:

- os
- subprocess
- socket
- requests
- shutil
- eval
- exec

If any forbidden keyword is detected, execution is blocked.

---

### 3. Sandbox Executor

The code is executed inside a **separate subprocess** to isolate it from the main application.

Key protections:
- Timeout protection
- Separate execution environment
- Output capture

---

### 4. Runtime Monitoring

During execution the system monitors:

- Execution time
- Memory usage
- Runtime errors

---

### 5. Result Formatter

The system returns structured output in the following format:

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
### Security Layers

- Keyword blocking
- Process isolation
- Execution timeout
- Resource monitoring

These layers prevent most common attacks against code execution environments.

---
