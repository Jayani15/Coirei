# Vulnerability Detection AI Agent (SAST Lite)

## 🔍 Overview
This project scans code for security vulnerabilities using Bandit and an AI-based analyzer.

## 🚨 Detects
- SQL Injection
- Hardcoded Secrets
- Unsafe Functions

## ⚙️ Setup

```bash
pip install -r requirements.txt
Install Bandit:

pip install bandit
▶️ Run
python main.py
📊 Output

Generated in:

report.json
🧪 Sample Input

See sample_code.py

```

---

# ✅ Sample Output (`report.json`)

```json
{
    "file": "sample_code.py",
    "vulnerabilities": [
        {
            "type": "Possible SQL injection vector through string-based query construction.",
            "line": 5,
            "severity": "High",
            "code_snippet": "query = \"SELECT * FROM users WHERE id = \" + user_id",
            "explanation": "This issue occurs because Possible SQL injection vector..."
        }
    ]
}
```