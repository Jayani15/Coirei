def score_candidate(candidate, jd_text):
    jd_text = jd_text.lower()

    score = 0

    # Skill match (simple keyword match)
    skills = candidate.get("skills", [])
    for skill in skills:
        if skill.lower() in jd_text:
            score += 10

    # Experience weight
    experience = candidate.get("experience", 0)
    score += experience * 5

    return score