import os
import json
from parser import extract_text_from_pdf
from extractor import extract_resume_data
from scorer import score_candidate
from utils import load_resumes, load_jd

RESUME_FOLDER = "data/resumes"
JD_PATH = "data/jd.txt"
OUTPUT_PATH = "data/output.json"


def main():
    resumes = load_resumes(RESUME_FOLDER)
    jd_text = load_jd(JD_PATH)

    candidates = []

    for file in resumes:
        print(f"Processing {file}...")
        
        text = extract_text_from_pdf(file)
        structured_data = extract_resume_data(text)
        
        score = score_candidate(structured_data, jd_text)
        structured_data["score"] = score
        
        candidates.append(structured_data)

    # Sort by score
    candidates = sorted(candidates, key=lambda x: x["score"], reverse=True)

    # Save output
    with open(OUTPUT_PATH, "w") as f:
        json.dump(candidates, f, indent=4)

    print("\n✅ Ranking Complete! Check output.json")


if __name__ == "__main__":
    main()