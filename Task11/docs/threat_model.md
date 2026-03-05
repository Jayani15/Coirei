# Threat Model – Python Code Sandboxing System

## Overview

This document identifies potential security threats when executing arbitrary Python code and describes the mitigation strategies implemented in the sandbox.

Running user-submitted code is inherently risky because the code may attempt to perform malicious actions such as deleting files, executing system commands, or accessing the network.

The sandbox implements multiple defensive mechanisms to reduce these risks.

---

# 1. File System Attacks

## Threat

User code may attempt to modify or delete files on the system.

Example attack:

```python
import os
os.remove("important_file.txt")
```

or

```python
import shutil
shutil.rmtree("/")
```

## Mitigation

The sandbox blocks dangerous modules and functions including:

- `os`
- `shutil`
- `open`

Before execution, the code is scanned for these keywords. If detected, execution is rejected.

---

# 2. OS Command Execution

## Threat

Attackers may try to execute system commands.

Example:

```python
import os
os.system("rm -rf /")
```

or

```python
import subprocess
subprocess.run(["ls"])
```

## Mitigation

The sandbox blocks the following modules:

- `os`
- `subprocess`

This prevents execution of system commands.

---

# 3. Network Access

## Threat

User code may attempt to communicate with external systems.

Example:

```python
import socket
```

or

```python
import requests
requests.get("https://example.com")
```

This could allow data exfiltration or malicious activity.

## Mitigation

Network-related modules are blocked:

- `socket`
- `requests`

The sandbox prevents execution if these modules appear in the code.

---

# 4. Infinite Loops / CPU Exhaustion

## Threat

A user may submit code that never terminates.

Example:

```python
while True:
    pass
```

This could consume CPU resources indefinitely.

## Mitigation

The sandbox enforces a strict execution timeout.

Example implementation:

```
process.communicate(timeout=2)
```

If the program runs longer than the allowed time, the process is terminated.

---

# 5. Memory Exhaustion

## Threat

User code may attempt to allocate excessive memory.

Example:

```python
a = []
while True:
    a.append("A" * 1000000)
```

This can crash the system by exhausting memory.

## Mitigation

Memory usage is monitored using the `psutil` library.

The sandbox tracks the memory consumed by the execution process.

---

# 6. Runtime Errors

## Threat

User code may contain errors such as:

- division by zero
- undefined variables
- invalid syntax

Example:

```python
print(10/0)
```

## Mitigation

The sandbox captures runtime errors and returns them safely in the response.

---

# Conclusion

The sandbox protects against the following threats:

- File system manipulation
- OS command execution
- Network access
- Infinite loops
- Memory abuse

These protections are implemented through:

- Keyword filtering
- Subprocess isolation
- Execution time limits
- Runtime monitoring

While this sandbox provides a strong baseline for secure code execution, additional security measures such as containerization and syscall filtering could further enhance protection.