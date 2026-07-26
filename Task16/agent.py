from tools import run_bandit
from analyzer import analyze_results, save_report

def read_file(file_path):
    with open(file_path, "r") as f:
        return f.read()

def run_agent(file_path):
    code = read_file(file_path)
    bandit_output = run_bandit(file_path)

    report = analyze_results(code, bandit_output, file_path)

    print("REPORT:", report)   # 👈 ADD THIS

    save_report(report)
    return report