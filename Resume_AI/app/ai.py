import json
import os
import re
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from groq import Groq

from .roles import ROLE_PROFILES
from .vector_db import search_candidate_knowledge


load_dotenv()


# ============================================================
# GROQ CONFIGURATION
# ============================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in .env")


client = Groq(
    api_key=GROQ_API_KEY
)

MODEL_NAME = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile"
)


# ============================================================
# GENERIC AI HELPERS
# ============================================================

def call_ai(
    prompt: str,
    temperature: float = 0.2
) -> str:
    """
    Send a prompt to Groq and return the text response.
    """

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI candidate intelligence assistant. "
                    "Return accurate, structured and concise answers. "
                    "Never invent candidate information."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=temperature
    )

    return response.choices[0].message.content.strip()


def extract_json(text: str) -> Dict[str, Any]:
    """
    Extract JSON from an AI response.

    Handles responses wrapped in markdown code fences.
    """

    text = text.strip()

    # Remove markdown fences
    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    # Direct JSON
    try:
        result = json.loads(text)

        if isinstance(result, dict):
            return result

    except json.JSONDecodeError:
        pass

    # Find first JSON object
    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1 and end > start:

        candidate = text[start:end + 1]

        try:
            result = json.loads(candidate)

            if isinstance(result, dict):
                return result

        except json.JSONDecodeError:
            pass

    raise ValueError(
        "AI response did not contain valid JSON."
    )


# ============================================================
# RESUME PARSING
# ============================================================

def parse_resume_with_ai(
    resume_text: str
) -> Dict[str, Any]:
    """
    Convert raw resume text into a structured candidate profile.
    """

    prompt = f"""
Analyze the following resume and extract ONLY information
that is explicitly supported by the resume.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "name": "",
    "email": "",
    "phone": "",
    "location": "",
    "education": [],
    "experience": [],
    "skills": [],
    "projects": [],
    "certifications": [],
    "training": [],
    "tools": [],
    "achievements": [],
    "career_preferences": {{}}
}}

Rules:

1. Do not invent information.
2. If information is absent, use an empty list or empty string.
3. Preserve important technical details.
4. For experience and projects, retain technologies,
   responsibilities and outcomes when available.
5. career_preferences should contain only preferences explicitly
   stated in the resume.
6. Return JSON only.

RESUME:
{resume_text}
"""

    raw_response = call_ai(
        prompt,
        temperature=0.1
    )

    data = extract_json(raw_response)

    # Guarantee expected keys exist
    expected_fields = [
        "name",
        "email",
        "phone",
        "location",
        "education",
        "experience",
        "skills",
        "projects",
        "certifications",
        "training",
        "tools",
        "achievements",
        "career_preferences"
    ]

    for field in expected_fields:

        if field not in data:

            if field in [
                "education",
                "experience",
                "skills",
                "projects",
                "certifications",
                "training",
                "tools",
                "achievements"
            ]:
                data[field] = []

            elif field == "career_preferences":
                data[field] = {}

            else:
                data[field] = ""

    return data


# ============================================================
# PROFILE COMPLETENESS
# ============================================================

PROFILE_WEIGHTS = {
    "identity": 0.05,
    "education": 0.15,
    "experience": 0.20,
    "skills": 0.15,
    "projects": 0.20,
    "certifications": 0.05,
    "training": 0.05,
    "tools": 0.05,
    "achievements": 0.05
}


def calculate_profile_completeness(
    profile: Dict[str, Any]
) -> float:
    """
    Calculate a weighted candidate-profile completeness score.

    Returns a value between 0 and 100.
    """

    scores = {}

    # Identity
    identity_fields = [
        profile.get("name"),
        profile.get("email")
    ]

    identity_count = sum(
        1 for value in identity_fields
        if value
    )

    scores["identity"] = identity_count / 2

    # List-based sections
    list_fields = [
        "education",
        "experience",
        "skills",
        "projects",
        "certifications",
        "training",
        "tools",
        "achievements"
    ]

    for field in list_fields:

        value = profile.get(field)

        if isinstance(value, list) and len(value) > 0:
            scores[field] = 1.0
        else:
            scores[field] = 0.0

    weighted_score = 0.0

    for field, weight in PROFILE_WEIGHTS.items():

        weighted_score += (
            scores.get(field, 0.0) * weight
        )

    return round(
        weighted_score * 100,
        2
    )


# ============================================================
# GAP DETECTION
# ============================================================

def find_missing_data(
    profile: Dict[str, Any]
) -> List[str]:
    """
    Identify missing or weak candidate information.
    """

    gaps = []

    # Identity
    if not profile.get("name"):
        gaps.append("name")

    if not profile.get("email"):
        gaps.append("email")

    # Education
    if not profile.get("education"):
        gaps.append("education")

    # Experience
    if not profile.get("experience"):
        gaps.append("experience")

    # Skills
    if not profile.get("skills"):
        gaps.append("skills")

    # Projects
    if not profile.get("projects"):
        gaps.append("projects")

    # Supporting evidence
    if not profile.get("certifications"):
        gaps.append("certifications")

    if not profile.get("training"):
        gaps.append("training")

    if not profile.get("tools"):
        gaps.append("tools")

    if not profile.get("achievements"):
        gaps.append("achievements")

    return gaps


def get_profile_status(
    completeness: float
) -> str:

    if completeness >= 90:
        return "complete"

    if completeness >= 70:
        return "mostly_complete"

    if completeness >= 40:
        return "partially_complete"

    return "incomplete"


# ============================================================
# GAP-FILLING QUESTIONS
# ============================================================

def generate_gap_question(
    profile: Dict[str, Any],
    missing_fields: List[str]
) -> Optional[Dict[str, str]]:
    """
    Generate the next most useful question for completing
    the candidate profile.
    """

    if not missing_fields:
        return None

    prompt = f"""
You are completing a candidate profile from a resume.

Candidate profile:
{json.dumps(profile, indent=2, ensure_ascii=False)}

Missing or weak fields:
{json.dumps(missing_fields)}

Choose ONE field that should be clarified next.

Ask one natural, specific question that helps collect
useful information for that field.

Return ONLY valid JSON:

{{
    "field": "field_name",
    "question": "question for the candidate"
}}

Do not ask about information that is already available.
Do not invent candidate facts.
"""

    response = call_ai(
        prompt,
        temperature=0.3
    )

    data = extract_json(response)

    return {
        "field": data.get(
            "field",
            missing_fields[0]
        ),
        "question": data.get(
            "question",
            f"Please provide more information about {missing_fields[0]}."
        )
    }


# ============================================================
# APPLY GAP-FILLING ANSWER
# ============================================================

def apply_gap_answer(
    profile: Dict[str, Any],
    field: str,
    answer: str
) -> Dict[str, Any]:
    """
    Convert a candidate's natural-language answer into
    structured profile information.
    """

    prompt = f"""
You are updating a candidate profile.

Current candidate profile:
{json.dumps(profile, indent=2, ensure_ascii=False)}

Field to update:
{field}

Candidate answer:
{answer}

Return ONLY valid JSON containing:

{{
    "updated_value": <value>
}}

Rules:

1. Extract only information contained in the candidate answer.
2. Do not invent facts.
3. If the field is a list, return a list.
4. If the field is an object, return an object.
5. Preserve useful technical details.
"""

    response = call_ai(
        prompt,
        temperature=0.1
    )

    data = extract_json(response)

    updated_value = data.get(
        "updated_value"
    )

    if updated_value is None:
        updated_value = answer

    # Work on a copy
    updated_profile = dict(profile)

    existing_value = updated_profile.get(field)

    # Merge list fields
    if isinstance(existing_value, list):

        if isinstance(updated_value, list):
            updated_profile[field] = (
                existing_value + updated_value
            )
        else:
            updated_profile[field] = (
                existing_value + [updated_value]
            )

    # Merge dictionaries
    elif isinstance(existing_value, dict):

        if isinstance(updated_value, dict):

            merged = dict(existing_value)
            merged.update(updated_value)

            updated_profile[field] = merged

        else:
            updated_profile[field] = updated_value

    else:
        updated_profile[field] = updated_value

    return updated_profile


# ============================================================
# ROLE RECOMMENDATION
# ============================================================

def _profile_text(
    profile: Dict[str, Any]
) -> str:

    return json.dumps(
        profile,
        indent=2,
        ensure_ascii=False
    )


def recommend_roles(
    candidate_id: int,
    profile: Dict[str, Any],
    top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Recommend the most suitable roles using:

    Candidate profile
    +
Candidate RAG evidence
    +
Role requirements
    """

    candidate_text = _profile_text(profile)

    recommendations = []

    # Retrieve candidate evidence once
    try:
        evidence = search_candidate_knowledge(
            candidate_id=candidate_id,
            query="candidate skills experience projects technical abilities",
            limit=8
        )

    except Exception:
        evidence = []

    evidence_text = "\n".join(
        item.get("text", "")
        for item in evidence
    )

    for role_name, role_data in ROLE_PROFILES.items():

        role_skills = role_data.get(
            "skills",
            []
        )

        role_competencies = role_data.get(
            "competencies",
            []
        )

        prompt = f"""
Evaluate how suitable this candidate is for the role.

CANDIDATE PROFILE:
{candidate_text}

RETRIEVED CANDIDATE EVIDENCE:
{evidence_text}

TARGET ROLE:
{role_name}

ROLE SKILLS:
{json.dumps(role_skills)}

ROLE COMPETENCIES:
{json.dumps(role_competencies)}

Return ONLY valid JSON:

{{
    "match_score": 0,
    "reason": "",
    "missing_skills": []
}}

Scoring:

90-100 = excellent match
80-89 = strong match
70-79 = good match
60-69 = moderate match
below 60 = weak match

Use only evidence supported by the candidate profile.
"""

        try:

            response = call_ai(
                prompt,
                temperature=0.1
            )

            result = extract_json(response)

            score = float(
                result.get(
                    "match_score",
                    0
                )
            )

            score = max(
                0,
                min(
                    100,
                    score
                )
            )

            recommendations.append({
                "role": role_name,
                "match_score": round(
                    score,
                    2
                ),
                "reason": result.get(
                    "reason",
                    "Based on the candidate profile."
                ),
                "missing_skills": result.get(
                    "missing_skills",
                    []
                )
            })

        except Exception:

            # Safe fallback using keyword overlap
            candidate_lower = candidate_text.lower()

            matched = [
                skill
                for skill in role_skills
                if skill.lower() in candidate_lower
            ]

            score = (
                len(matched) /
                max(len(role_skills), 1)
            ) * 100

            recommendations.append({
                "role": role_name,
                "match_score": round(
                    score,
                    2
                ),
                "reason": (
                    f"{len(matched)} of the role's "
                    f"key skills were found in the "
                    f"candidate profile."
                ),
                "missing_skills": [
                    skill
                    for skill in role_skills
                    if skill not in matched
                ]
            })

    recommendations.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    return recommendations[:top_k]


# ============================================================
# ASSESSMENT COMPETENCY GENERATION
# ============================================================

def get_role_competencies(
    role_name: str
) -> List[str]:

    role = ROLE_PROFILES.get(
        role_name
    )

    if not role:
        return [
            "technical fundamentals",
            "problem solving",
            "practical implementation"
        ]

    return role.get(
        "competencies",
        []
    )


def choose_next_competency(
    role_name: str,
    evaluations: List[Dict[str, Any]]
) -> str:

    competencies = get_role_competencies(
        role_name
    )

    if not competencies:
        return "technical fundamentals"

    evaluated = {
        evaluation.get("competency")
        for evaluation in evaluations
    }

    # First cover competencies not yet assessed
    for competency in competencies:

        if competency not in evaluated:
            return competency

    # Otherwise ask about the weakest area
    weakest = min(
        evaluations,
        key=lambda x: x.get("score", 10)
    )

    return weakest.get(
        "competency",
        competencies[0]
    )


# ============================================================
# DIFFICULTY ADAPTATION
# ============================================================

def determine_difficulty(
    evaluations: List[Dict[str, Any]]
) -> str:

    if not evaluations:
        return "medium"

    latest_score = evaluations[-1].get(
        "score",
        5
    )

    if latest_score >= 8:
        return "hard"

    if latest_score >= 5:
        return "medium"

    return "easy"


# ============================================================
# ADAPTIVE QUESTION GENERATION
# ============================================================

def generate_adaptive_question(
    candidate_id: int,
    profile: Dict[str, Any],
    role_name: str,
    evaluations: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, str]:
    """
    Generate a role-specific adaptive assessment question.
    """

    evaluations = evaluations or []

    competency = choose_next_competency(
        role_name,
        evaluations
    )

    difficulty = determine_difficulty(
        evaluations
    )

    # Retrieve evidence relevant to this question
    try:

        evidence = search_candidate_knowledge(
            candidate_id=candidate_id,
            query=(
                f"{role_name} {competency} "
                "candidate experience projects skills"
            ),
            limit=5
        )

    except Exception:
        evidence = []

    evidence_text = "\n".join(
        item.get("text", "")
        for item in evidence
    )

    previous_questions = [
        evaluation.get("question", "")
        for evaluation in evaluations
    ]

    prompt = f"""
Create ONE technical assessment question.

CANDIDATE PROFILE:
{json.dumps(profile, indent=2, ensure_ascii=False)}

TARGET ROLE:
{role_name}

COMPETENCY:
{competency}

DIFFICULTY:
{difficulty}

RELEVANT CANDIDATE EVIDENCE:
{evidence_text}

PREVIOUS QUESTIONS:
{json.dumps(previous_questions, ensure_ascii=False)}

Requirements:

1. Ask exactly ONE question.
2. The question must be relevant to {role_name}.
3. Focus on {competency}.
4. Use the candidate's background when useful.
5. Do not ask a duplicate of a previous question.
6. Difficulty must match {difficulty}.
7. Do not assume skills that aren't supported by the profile.

Return ONLY JSON:

{{
    "question": "",
    "competency": "{competency}",
    "difficulty": "{difficulty}"
}}
"""

    response = call_ai(
        prompt,
        temperature=0.5
    )

    data = extract_json(response)

    return {
        "question": data.get(
            "question",
            f"Explain an important concept related to {competency}."
        ),
        "competency": data.get(
            "competency",
            competency
        ),
        "difficulty": data.get(
            "difficulty",
            difficulty
        )
    }


# ============================================================
# ANSWER EVALUATION
# ============================================================

def evaluate_answer(
    question: str,
    answer: str,
    role_name: Optional[str] = None,
    competency: Optional[str] = None,
    difficulty: Optional[str] = None,
    candidate_profile: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Evaluate a candidate answer from 0 to 10.
    """

    role_name = role_name or "Technical Role"

    competency = (
        competency
        or "technical fundamentals"
    )

    difficulty = (
        difficulty
        or "medium"
    )

    prompt = f"""
Evaluate the candidate's answer.

TARGET ROLE:
{role_name}

COMPETENCY:
{competency}

DIFFICULTY:
{difficulty}

QUESTION:
{question}

CANDIDATE ANSWER:
{answer}

Candidate profile:
{json.dumps(candidate_profile or {}, ensure_ascii=False)}

Evaluate:

- correctness
- technical depth
- relevance
- reasoning
- clarity
- practical understanding

Return ONLY JSON:

{{
    "score": 0,
    "feedback": "",
    "explanation": ""
}}

Score from 0 to 10.

0-2: incorrect or almost no understanding
3-4: weak understanding
5-6: basic acceptable understanding
7-8: good understanding
9-10: excellent understanding

Do not give credit for information that is not actually
demonstrated by the answer.
"""

    response = call_ai(
        prompt,
        temperature=0.1
    )

    data = extract_json(response)

    score = float(
        data.get(
            "score",
            0
        )
    )

    score = max(
        0,
        min(
            10,
            score
        )
    )

    return {
        "score": round(score, 2),

        "feedback": data.get(
            "feedback",
            ""
        ),

        "explanation": data.get(
            "explanation",
            ""
        )
    }


# ============================================================
# SEMANTIC ROLE SIMILARITY
# ============================================================

def calculate_role_similarity(
    candidate_id: int,
    role_name: str
) -> float:
    """
    Estimate semantic similarity between the candidate's
    stored knowledge and the selected role.
    """

    role = ROLE_PROFILES.get(
        role_name
    )

    if not role:
        return 0.0

    role_text = " ".join(
        role.get("skills", []) +
        role.get("competencies", [])
    )

    try:

        results = search_candidate_knowledge(
            candidate_id=candidate_id,
            query=role_text,
            limit=5
        )

        if not results:
            return 0.0

        scores = [
            float(result.get("score", 0))
            for result in results
        ]

        similarity = sum(scores) / len(scores)

        return round(
            max(
                0,
                min(
                    100,
                    similarity * 100
                )
            ),
            2
        )

    except Exception:
        return 0.0


# ============================================================
# READINESS BENCHMARK
# ============================================================

def generate_readiness_benchmark(
    candidate_id: int,
    profile: Dict[str, Any],
    role_name: str,
    evaluations: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Generate a candidate readiness benchmark against
    a selected target role.
    """

    scores = [
        float(evaluation.get("score", 0))
        for evaluation in evaluations
        if evaluation.get("score") is not None
    ]

    assessment_average = (
        sum(scores) / len(scores)
        if scores
        else 0
    )

    profile_completeness = (
        calculate_profile_completeness(
            profile
        )
    )

    semantic_similarity = (
        calculate_role_similarity(
            candidate_id,
            role_name
        )
    )

    prompt = f"""
Calculate a candidate's readiness for a target job role.

TARGET ROLE:
{role_name}

CANDIDATE PROFILE:
{json.dumps(profile, indent=2, ensure_ascii=False)}

ASSESSMENT SCORES:
{json.dumps(evaluations, indent=2, ensure_ascii=False)}

PROFILE COMPLETENESS:
{profile_completeness}

ASSESSMENT AVERAGE:
{assessment_average}

SEMANTIC ROLE SIMILARITY:
{semantic_similarity}

Return ONLY JSON:

{{
    "technical_fundamentals": 0,
    "role_specific_knowledge": 0,
    "practical_implementation": 0,
    "problem_solving": 0,
    "project_depth": 0,
    "conceptual_clarity": 0,
    "overall_readiness": 0,
    "improvement_gaps": [],
    "feedback": ""
}}

All scores must be between 0 and 100.

Base the metrics on the available evidence.
Do not invent achievements or skills.

overall_readiness should represent how prepared
the candidate currently appears for the selected role.
"""

    response = call_ai(
        prompt,
        temperature=0.1
    )

    data = extract_json(response)

    metric_names = [
        "technical_fundamentals",
        "role_specific_knowledge",
        "practical_implementation",
        "problem_solving",
        "project_depth",
        "conceptual_clarity",
        "overall_readiness"
    ]

    readiness_metrics = {}

    for metric in metric_names:

        value = float(
            data.get(
                metric,
                0
            )
        )

        readiness_metrics[metric] = round(
            max(
                0,
                min(
                    100,
                    value
                )
            ),
            2
        )

    # Fallback overall score if AI fails to provide a useful one
    if readiness_metrics["overall_readiness"] == 0:

        readiness_metrics["overall_readiness"] = round(
            (
                assessment_average * 10
                + profile_completeness
                + semantic_similarity
            ) / 3,
            2
        )

    return {
        "readiness_metrics": readiness_metrics,

        "improvement_gaps": data.get(
            "improvement_gaps",
            []
        ),

        "feedback": data.get(
            "feedback",
            "Readiness benchmark generated successfully."
        ),

        "semantic_similarity": semantic_similarity
    }


# ============================================================
# TECHNICAL LEVEL
# ============================================================

def get_technical_level(
    score: float
) -> str:

    if score >= 85:
        return "Advanced"

    if score >= 70:
        return "Intermediate"

    if score >= 50:
        return "Developing"

    return "Beginner"