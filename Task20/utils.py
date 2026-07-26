import json
import os


def save_json(data, filepath):
    os.makedirs("output", exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def save_report(data, filepath):
    os.makedirs("output", exist_ok=True)

    report = f"""
COMPLAINT DECISION REPORT
=========================

Category       : {data.get("category")}
Sentiment      : {data.get("sentiment")}
Urgency Level  : {data.get("urgency_level")}
Decision       : {data.get("decision")}
Priority Score : {data.get("priority_score")}

Justification:
{data.get("justification")}
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report)