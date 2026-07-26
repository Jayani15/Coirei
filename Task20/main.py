from agent import process_complaint
from utils import save_json, save_report

def main():
    complaint = input("Enter customer complaint:\n\n")

    result = process_complaint(complaint)

    print("\nFinal Result:\n")
    print(result)

    save_json(result, "output/result.json")
    save_report(result, "output/report.txt")

    print("\nSaved to output folder.")

if __name__ == "__main__":
    main()