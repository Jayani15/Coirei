from agent.agent import WebTestingAgent
from utils.report import generate_report
from utils.llm_analysis import analyze_report

def run_test(url):
    agent = WebTestingAgent()

    results = agent.run(url)

    report = generate_report(
        url,
        results["broken_links"],
        results["button_results"],
        results["screenshot"]
    )

    ai_analysis = analyze_report(report)

    print("\n===== FINAL REPORT =====\n")
    print(report)

    print("\n===== AI ANALYSIS =====\n")
    print(ai_analysis)


if __name__ == "__main__":
    url = input("Enter website URL: ")
    run_test(url)