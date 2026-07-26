import json

def classify_severity(issue_text):
    issue_text = issue_text.lower()

    if "sql" in issue_text:
        return "High"
    elif "password" in issue_text or "key" in issue_text:
        return "Critical"
    elif "exec" in issue_text or "eval" in issue_text:
        return "High"
    else:
        return "Medium"


def generate_explanation(issue_text):
    return f"This issue occurs because {issue_text}. It may lead to security risks if not fixed."


def analyze_results(code, bandit_output, file_path):
    vulnerabilities = []

    issues = bandit_output.get("results", [])

    for issue in issues:
        vuln = {
            "type": issue.get("issue_text", "Unknown"),
            "line": issue.get("line_number"),
            "severity": classify_severity(issue.get("issue_text", "")),
            "code_snippet": issue.get("code"),
            "explanation": generate_explanation(issue.get("issue_text", ""))
        }
        vulnerabilities.append(vuln)

    return {
        "file": file_path,
        "vulnerabilities": vulnerabilities
    }


def save_report(report):
    with open("report.json", "w") as f:
        json.dump(report, f, indent=4)