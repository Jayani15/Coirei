import json
from datetime import datetime

def generate_report(url, broken_links, button_results, screenshot):
    report = {
        "timestamp": str(datetime.now()),
        "url": url,
        "broken_links": broken_links,
        "button_results": button_results,
        "screenshot": screenshot
    }

    with open("report.json", "w") as f:
        json.dump(report, f, indent=4)

    return report