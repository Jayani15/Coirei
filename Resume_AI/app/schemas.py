from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class CandidateResponse(BaseModel):
    id: int

    name: Optional[str] = None

    email: Optional[str] = None

    resume_data: Dict[str, Any]

    missing_data: List[str] = []

    career_preferences: Dict[str, Any] = {}

    preferred_roles: List[str] = []

    profile_completeness: float = 0

    profile_status: str = "incomplete"


class ResumeUploadResponse(BaseModel):
    candidate_id: int

    message: str

    resume_data: Dict[str, Any]

    missing_data: List[str]

    profile_completeness: float

    profile_status: str


class GapQuestionResponse(BaseModel):
    candidate_id: int

    question: Optional[str] = None

    field: Optional[str] = None

    profile_completeness: float

    completed: bool


class GapAnswerRequest(BaseModel):
    field: str = Field(..., min_length=1)

    answer: str = Field(..., min_length=1)


class GapAnswerResponse(BaseModel):
    candidate_id: int

    message: str

    updated_profile: Dict[str, Any]

    missing_data: List[str]

    profile_completeness: float

    profile_status: str

    next_question: Optional[str] = None

    completed: bool


class RoleRecommendationResponse(BaseModel):
    role: str

    match_score: float

    reason: str

    missing_skills: List[str] = []


class RoleSelectionRequest(BaseModel):
    roles: List[str] = Field(
        ...,
        min_length=1,
        max_length=3
    )


class RoleSelectionResponse(BaseModel):
    candidate_id: int

    selected_roles: List[str]

    message: str


class AssessmentStartResponse(BaseModel):
    assessment_id: int

    candidate_id: int

    target_role: str

    question: str

    competency: str

    difficulty: str


class AnswerRequest(BaseModel):
    answer: str = Field(..., min_length=1)


class AnswerResponse(BaseModel):
    evaluation_id: int

    score: float

    feedback: str

    explanation: str

    next_question: Optional[str] = None

    completed: bool


class EvaluationResponse(BaseModel):
    question: str

    answer: Optional[str]

    score: Optional[float]

    feedback: Optional[str]

    explanation: Optional[str]

    competency: Optional[str]

    difficulty: Optional[str]


class AssessmentResult(BaseModel):
    assessment_id: int

    candidate_id: int

    target_role: Optional[str]

    score: float

    technical_level: str

    semantic_similarity: float

    readiness_metrics: Dict[str, float]

    improvement_gaps: List[str]

    feedback: str

    evaluations: List[EvaluationResponse]