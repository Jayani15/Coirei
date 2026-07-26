import subprocess
import json

def run_bandit(file_path):
    try:
        result = subprocess.run(
            ["bandit", "-r", file_path, "-f", "json"],
            capture_output=True,
            text=True
        )

        if result.stdout:
            return json.loads(result.stdout)
        else:
            return {}

    except Exception as e:
        print("Error running Bandit:", e)
        return {}