from typing import List, Optional

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
)
from sqlalchemy.orm import Session

from .ai import (
    apply_gap_answer,
    calculate_profile_completeness,
    find_missing_data,
    generate_adaptive_question,
    generate_gap_question,
    generate_readiness_benchmark,
    get_profile_status,
    get_technical_level,
    parse_resume_with_ai,
    recommend_roles,
    evaluate_answer,
)
from .database import get_db
from .models import (
    Assessment,
    Candidate,
    Evaluation,
    GapConversation,
    RoleRecommendation,
)
from .parser import extract_text_from_pdf
from .roles import get_all_roles
from .schemas import (
    AnswerRequest,
    AnswerResponse,
    AssessmentResult,
    AssessmentStartResponse,
    CandidateResponse,
    EvaluationResponse,
    GapAnswerRequest,
    GapAnswerResponse,
    GapQuestionResponse,
    ResumeUploadResponse,
    RoleRecommendationResponse,
    RoleSelectionRequest,
    RoleSelectionResponse,
)
from .vector_db import store_candidate_profile


router = APIRouter()


# ============================================================
# RESUME UPLOAD
# ============================================================

@router.post(
    "/resume/upload",
    response_model=ResumeUploadResponse
)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a resume, parse it using AI, detect gaps,
    calculate completeness and store candidate evidence in Qdrant.
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file was provided."
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF resumes are supported."
        )

    upload_dir = "uploads"

    import os

    os.makedirs(
        upload_dir,
        exist_ok=True
    )

    file_path = os.path.join(
        upload_dir,
        file.filename
    )

    try:

        contents = await file.read()

        with open(
            file_path,
            "wb"
        ) as buffer:
            buffer.write(contents)

        resume_text = extract_text_from_pdf(
            file_path
        )

        if not resume_text.strip():
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from the PDF."
            )

        # ----------------------------------------------------
        # AI RESUME PARSING
        # ----------------------------------------------------

        resume_data = parse_resume_with_ai(
            resume_text
        )

        # ----------------------------------------------------
        # PROFILE ANALYSIS
        # ----------------------------------------------------

        missing_data = find_missing_data(
            resume_data
        )

        completeness = calculate_profile_completeness(
            resume_data
        )

        profile_status = get_profile_status(
            completeness
        )

        # ----------------------------------------------------
        # CREATE CANDIDATE
        # ----------------------------------------------------

        candidate = Candidate(
            name=resume_data.get("name"),
            email=resume_data.get("email"),

            resume_data=resume_data,

            missing_data=missing_data,

            career_preferences=resume_data.get(
                "career_preferences",
                {}
            ),

            preferred_roles=[],

            profile_completeness=completeness,

            profile_status=profile_status
        )

        db.add(candidate)

        db.commit()

        db.refresh(candidate)

        # ----------------------------------------------------
        # STORE CANDIDATE KNOWLEDGE IN QDRANT
        # ----------------------------------------------------

        try:

            store_candidate_profile(
                candidate_id=candidate.id,
                resume_data=resume_data
            )

        except Exception as exc:

            print(
                f"Warning: Qdrant storage failed: {exc}"
            )

        return ResumeUploadResponse(
            candidate_id=candidate.id,

            message=(
                "Resume uploaded and candidate profile "
                "created successfully."
            ),

            resume_data=resume_data,

            missing_data=missing_data,

            profile_completeness=completeness,

            profile_status=profile_status
        )

    finally:

        # Keep uploaded resume for now.
        # It can be deleted later if required.
        pass


# ============================================================
# GET CANDIDATE PROFILE
# ============================================================

@router.get(
    "/candidate/{candidate_id}",
    response_model=CandidateResponse
)
def get_candidate_profile(
    candidate_id: int,
    db: Session = Depends(get_db)
):
    """
    Return the complete candidate profile.
    """

    candidate = (
        db.query(Candidate)
        .filter(
            Candidate.id == candidate_id
        )
        .first()
    )

    if not candidate:

        raise HTTPException(
            status_code=404,
            detail="Candidate not found."
        )

    return CandidateResponse(
        id=candidate.id,

        name=candidate.name,

        email=candidate.email,

        resume_data=candidate.resume_data or {},

        missing_data=candidate.missing_data or [],

        career_preferences=(
            candidate.career_preferences or {}
        ),

        preferred_roles=(
            candidate.preferred_roles or []
        ),

        profile_completeness=(
            candidate.profile_completeness or 0
        ),

        profile_status=(
            candidate.profile_status or "incomplete"
        )
    )


# ============================================================
# GAP QUESTION
# ============================================================

@router.get(
    "/candidate/{candidate_id}/gap-question",
    response_model=GapQuestionResponse
)
def get_gap_question(
    candidate_id: int,
    db: Session = Depends(get_db)
):
    """
    Generate the next question required to complete
    the candidate profile.
    """

    candidate = (
        db.query(Candidate)
        .filter(
            Candidate.id == candidate_id
        )
        .first()
    )

    if not candidate:

        raise HTTPException(
            status_code=404,
            detail="Candidate not found."
        )

    profile = candidate.resume_data or {}

    # Recalculate instead of trusting an old value
    completeness = calculate_profile_completeness(
        profile
    )

    missing_data = find_missing_data(
        profile
    )

    candidate.missing_data = missing_data

    candidate.profile_completeness = completeness

    candidate.profile_status = get_profile_status(
        completeness
    )

    db.commit()

    if not missing_data:

        return GapQuestionResponse(
            candidate_id=candidate_id,

            question=None,

            field=None,

            profile_completeness=completeness,

            completed=True
        )

    question_data = generate_gap_question(
        profile=profile,

        missing_fields=missing_data
    )

    if not question_data:

        return GapQuestionResponse(
            candidate_id=candidate_id,

            question=None,

            field=None,

            profile_completeness=completeness,

            completed=True
        )

    # Save the question
    conversation = GapConversation(
        candidate_id=candidate_id,

        field=question_data["field"],

        question=question_data["question"],

        answer=None
    )

    db.add(conversation)

    db.commit()

    return GapQuestionResponse(
        candidate_id=candidate_id,

        question=question_data["question"],

        field=question_data["field"],

        profile_completeness=completeness,

        completed=False
    )


# ============================================================
# GAP ANSWER
# ============================================================

@router.post(
    "/candidate/{candidate_id}/gap-answer",
    response_model=GapAnswerResponse
)
def submit_gap_answer(
    candidate_id: int,
    request: GapAnswerRequest,
    db: Session = Depends(get_db)
):
    """
    Save a candidate's answer, update the structured profile,
    recalculate completeness and generate the next question.
    """

    candidate = (
        db.query(Candidate)
        .filter(
            Candidate.id == candidate_id
        )
        .first()
    )

    if not candidate:

        raise HTTPException(
            status_code=404,
            detail="Candidate not found."
        )

    profile = dict(
        candidate.resume_data or {}
    )

    # --------------------------------------------------------
    # UPDATE PROFILE USING AI
    # --------------------------------------------------------

    updated_profile = apply_gap_answer(
        profile=profile,

        field=request.field,

        answer=request.answer
    )

    # --------------------------------------------------------
    # RECALCULATE PROFILE
    # --------------------------------------------------------

    missing_data = find_missing_data(
        updated_profile
    )

    completeness = calculate_profile_completeness(
        updated_profile
    )

    profile_status = get_profile_status(
        completeness
    )

    candidate.resume_data = updated_profile

    candidate.missing_data = missing_data

    candidate.profile_completeness = completeness

    candidate.profile_status = profile_status

    # Update career preferences if they were supplied
    if request.field == "career_preferences":

        candidate.career_preferences = (
            updated_profile.get(
                "career_preferences",
                {}
            )
        )

    # --------------------------------------------------------
    # SAVE CONVERSATION ANSWER
    # --------------------------------------------------------

    conversation = (
        db.query(GapConversation)
        .filter(
            GapConversation.candidate_id == candidate_id,

            GapConversation.field == request.field,

            GapConversation.answer.is_(None)
        )
        .order_by(
            GapConversation.id.desc()
        )
        .first()
    )

    if conversation:

        conversation.answer = request.answer

    else:

        conversation = GapConversation(
            candidate_id=candidate_id,

            field=request.field,

            question=(
                f"Please provide information about "
                f"{request.field}."
            ),

            answer=request.answer
        )

        db.add(conversation)

    db.commit()

    # --------------------------------------------------------
    # UPDATE RAG
    # --------------------------------------------------------

    try:

        store_candidate_profile(
            candidate_id=candidate_id,

            resume_data=updated_profile
        )

    except Exception as exc:

        print(
            f"Warning: Qdrant update failed: {exc}"
        )

    # --------------------------------------------------------
    # NEXT QUESTION
    # --------------------------------------------------------

    if not missing_data:

        return GapAnswerResponse(
            candidate_id=candidate_id,

            message=(
                "Candidate profile is now complete."
            ),

            updated_profile=updated_profile,

            missing_data=[],

            profile_completeness=completeness,

            profile_status=profile_status,

            next_question=None,

            completed=True
        )

    next_question_data = generate_gap_question(
        profile=updated_profile,

        missing_fields=missing_data
    )

    next_question = None

    if next_question_data:

        next_question = (
            next_question_data["question"]
        )

        db.add(
            GapConversation(
                candidate_id=candidate_id,

                field=next_question_data["field"],

                question=next_question,

                answer=None
            )
        )

        db.commit()

    return GapAnswerResponse(
        candidate_id=candidate_id,

        message=(
            "Candidate profile updated successfully."
        ),

        updated_profile=updated_profile,

        missing_data=missing_data,

        profile_completeness=completeness,

        profile_status=profile_status,

        next_question=next_question,

        completed=False
    )


# ============================================================
# ROLE RECOMMENDATIONS
# ============================================================

@router.get(
    "/candidate/{candidate_id}/recommendations",
    response_model=List[RoleRecommendationResponse]
)
def get_role_recommendations(
    candidate_id: int,
    db: Session = Depends(get_db)
):
    """
    Generate approximately five suitable job-role recommendations.
    """

    candidate = (
        db.query(Candidate)
        .filter(
            Candidate.id == candidate_id
        )
        .first()
    )

    if not candidate:

        raise HTTPException(
            status_code=404,
            detail="Candidate not found."
        )

    profile = candidate.resume_data or {}

    recommendations = recommend_roles(
        candidate_id=candidate_id,

        profile=profile,

        top_k=5
    )

    # Remove old recommendations
    (
        db.query(RoleRecommendation)
        .filter(
            RoleRecommendation.candidate_id
            == candidate_id
        )
        .delete(
            synchronize_session=False
        )
    )

    # Store new recommendations
    for recommendation in recommendations:

        db.add(
            RoleRecommendation(
                candidate_id=candidate_id,

                role=recommendation["role"],

                match_score=recommendation[
                    "match_score"
                ],

                reason=recommendation["reason"],

                missing_skills=recommendation[
                    "missing_skills"
                ]
            )
        )

    db.commit()

    return recommendations


# ============================================================
# ROLE SELECTION
# ============================================================

@router.post(
    "/candidate/{candidate_id}/roles",
    response_model=RoleSelectionResponse
)
def select_roles(
    candidate_id: int,
    request: RoleSelectionRequest,
    db: Session = Depends(get_db)
):
    """
    Save 1-3 preferred roles selected by the candidate.
    """

    candidate = (
        db.query(Candidate)
        .filter(
            Candidate.id == candidate_id
        )
        .first()
    )

    if not candidate:

        raise HTTPException(
            status_code=404,
            detail="Candidate not found."
        )

    available_roles = set(
        get_all_roles()
    )

    invalid_roles = [
        role
        for role in request.roles
        if role not in available_roles
    ]

    if invalid_roles:

        raise HTTPException(
            status_code=400,

            detail={
                "message": "Invalid role selected.",

                "invalid_roles": invalid_roles,

                "available_roles": list(
                    available_roles
                )
            }
        )

    # Remove duplicates while preserving order
    selected_roles = list(
        dict.fromkeys(
            request.roles
        )
    )

    if len(selected_roles) > 3:

        raise HTTPException(
            status_code=400,

            detail=(
                "You can select a maximum of "
                "3 preferred roles."
            )
        )

    candidate.preferred_roles = selected_roles

    db.commit()

    return RoleSelectionResponse(
        candidate_id=candidate_id,

        selected_roles=selected_roles,

        message=(
            "Preferred roles saved successfully."
        )
    )


# ============================================================
# START ASSESSMENT
# ============================================================

@router.post(
    "/assessment/start/{candidate_id}",
    response_model=AssessmentStartResponse
)
def start_assessment(
    candidate_id: int,
    target_role: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Start a role-specific adaptive assessment.

    target_role can be supplied as a query parameter.
    Example:
    /api/assessment/start/1?target_role=AI%20Engineer
    """

    candidate = (
        db.query(Candidate)
        .filter(
            Candidate.id == candidate_id
        )
        .first()
    )

    if not candidate:

        raise HTTPException(
            status_code=404,
            detail="Candidate not found."
        )

    preferred_roles = (
        candidate.preferred_roles or []
    )

    if target_role:

        if target_role not in get_all_roles():

            raise HTTPException(
                status_code=400,

                detail="Invalid target role."
            )

    elif preferred_roles:

        target_role = preferred_roles[0]

    else:

        raise HTTPException(
            status_code=400,

            detail=(
                "Please select a preferred role "
                "before starting the assessment."
            )
        )

    # --------------------------------------------------------
    # CREATE ASSESSMENT
    # --------------------------------------------------------

    assessment = Assessment(
        candidate_id=candidate_id,

        target_role=target_role,

        status="in_progress"
    )

    db.add(assessment)

    db.commit()

    db.refresh(assessment)

    # --------------------------------------------------------
    # GENERATE FIRST QUESTION
    # --------------------------------------------------------

    question_data = generate_adaptive_question(
        candidate_id=candidate_id,

        profile=candidate.resume_data or {},

        role_name=target_role,

        evaluations=[]
    )

    evaluation = Evaluation(
        assessment_id=assessment.id,

        question=question_data["question"],

        answer=None,

        score=None,

        feedback=None,

        explanation=None,

        competency=question_data["competency"],

        difficulty=question_data["difficulty"]
    )

    db.add(evaluation)

    db.commit()

    return AssessmentStartResponse(
        assessment_id=assessment.id,

        candidate_id=candidate_id,

        target_role=target_role,

        question=question_data["question"],

        competency=question_data["competency"],

        difficulty=question_data["difficulty"]
    )


# ============================================================
# SUBMIT ASSESSMENT ANSWER
# ============================================================

@router.post(
    "/assessment/{assessment_id}/answer",
    response_model=AnswerResponse
)
def submit_answer(
    assessment_id: int,
    request: AnswerRequest,
    db: Session = Depends(get_db)
):
    """
    Evaluate the current answer and generate the next
    adaptive question.
    """

    assessment = (
        db.query(Assessment)
        .filter(
            Assessment.id == assessment_id
        )
        .first()
    )

    if not assessment:

        raise HTTPException(
            status_code=404,
            detail="Assessment not found."
        )

    if assessment.status == "completed":

        raise HTTPException(
            status_code=400,
            detail="Assessment is already completed."
        )

    # --------------------------------------------------------
    # FIND CURRENT UNANSWERED QUESTION
    # --------------------------------------------------------

    current_evaluation = (
        db.query(Evaluation)
        .filter(
            Evaluation.assessment_id
            == assessment_id,

            Evaluation.answer.is_(None)
        )
        .order_by(
            Evaluation.id.desc()
        )
        .first()
    )

    if not current_evaluation:

        raise HTTPException(
            status_code=400,

            detail=(
                "No unanswered question is available."
            )
        )

    candidate = (
        db.query(Candidate)
        .filter(
            Candidate.id
            == assessment.candidate_id
        )
        .first()
    )

    if not candidate:

        raise HTTPException(
            status_code=404,
            detail="Candidate not found."
        )

    # --------------------------------------------------------
    # EVALUATE ANSWER
    # --------------------------------------------------------

    evaluation_result = evaluate_answer(
        question=current_evaluation.question,

        answer=request.answer,

        role_name=assessment.target_role,

        competency=current_evaluation.competency,

        difficulty=current_evaluation.difficulty,

        candidate_profile=(
            candidate.resume_data or {}
        )
    )

    current_evaluation.answer = request.answer

    current_evaluation.score = (
        evaluation_result["score"]
    )

    current_evaluation.feedback = (
        evaluation_result["feedback"]
    )

    current_evaluation.explanation = (
        evaluation_result["explanation"]
    )

    db.commit()

    # --------------------------------------------------------
    # ASSESSMENT LENGTH
    # --------------------------------------------------------

    answered_count = (
        db.query(Evaluation)
        .filter(
            Evaluation.assessment_id
            == assessment_id,

            Evaluation.answer.is_not(None)
        )
        .count()
    )

    MAX_QUESTIONS = 5

    if answered_count >= MAX_QUESTIONS:

        # -----------------------------------------------
        # FINISH ASSESSMENT
        # -----------------------------------------------

        evaluations_db = (
            db.query(Evaluation)
            .filter(
                Evaluation.assessment_id
                == assessment_id
            )
            .order_by(
                Evaluation.id
            )
            .all()
        )

        evaluations_data = [
            {
                "question": item.question,

                "answer": item.answer,

                "score": item.score,

                "feedback": item.feedback,

                "explanation": item.explanation,

                "competency": item.competency,

                "difficulty": item.difficulty
            }

            for item in evaluations_db
        ]

        benchmark = generate_readiness_benchmark(
            candidate_id=assessment.candidate_id,

            profile=candidate.resume_data or {},

            role_name=assessment.target_role,

            evaluations=evaluations_data
        )

        scores = [
            item["score"]
            for item in evaluations_data
            if item["score"] is not None
        ]

        final_score = (
            sum(scores) / len(scores)
            if scores
            else 0
        )

        technical_level = get_technical_level(
            final_score * 10
        )

        assessment.score = round(
            final_score,
            2
        )

        assessment.technical_level = (
            technical_level
        )

        assessment.feedback = (
            benchmark["feedback"]
        )

        assessment.readiness_metrics = (
            benchmark["readiness_metrics"]
        )

        assessment.improvement_gaps = (
            benchmark["improvement_gaps"]
        )

        assessment.status = "completed"

        db.commit()

        return AnswerResponse(
            evaluation_id=current_evaluation.id,

            score=evaluation_result["score"],

            feedback=evaluation_result["feedback"],

            explanation=evaluation_result["explanation"],

            next_question=None,

            completed=True
        )

    # --------------------------------------------------------
    # GENERATE NEXT ADAPTIVE QUESTION
    # --------------------------------------------------------

    previous_evaluations_db = (
        db.query(Evaluation)
        .filter(
            Evaluation.assessment_id
            == assessment_id
        )
        .order_by(
            Evaluation.id
        )
        .all()
    )

    previous_evaluations = [
        {
            "question": item.question,

            "answer": item.answer,

            "score": item.score,

            "feedback": item.feedback,

            "explanation": item.explanation,

            "competency": item.competency,

            "difficulty": item.difficulty
        }

        for item in previous_evaluations_db
        if item.answer is not None
    ]

    next_question_data = generate_adaptive_question(
        candidate_id=assessment.candidate_id,

        profile=candidate.resume_data or {},

        role_name=assessment.target_role,

        evaluations=previous_evaluations
    )

    next_evaluation = Evaluation(
        assessment_id=assessment_id,

        question=next_question_data["question"],

        answer=None,

        score=None,

        feedback=None,

        explanation=None,

        competency=next_question_data["competency"],

        difficulty=next_question_data["difficulty"]
    )

    db.add(next_evaluation)

    db.commit()

    return AnswerResponse(
        evaluation_id=current_evaluation.id,

        score=evaluation_result["score"],

        feedback=evaluation_result["feedback"],

        explanation=evaluation_result["explanation"],

        next_question=(
            next_question_data["question"]
        ),

        completed=False
    )


# ============================================================
# GET ASSESSMENT RESULT
# ============================================================

@router.get(
    "/assessment/{assessment_id}/result",
    response_model=AssessmentResult
)
def get_assessment_result(
    assessment_id: int,
    db: Session = Depends(get_db)
):
    """
    Return the complete readiness benchmark and
    assessment evaluation.
    """

    assessment = (
        db.query(Assessment)
        .filter(
            Assessment.id == assessment_id
        )
        .first()
    )

    if not assessment:

        raise HTTPException(
            status_code=404,
            detail="Assessment not found."
        )

    evaluations = (
        db.query(Evaluation)
        .filter(
            Evaluation.assessment_id
            == assessment_id
        )
        .order_by(
            Evaluation.id
        )
        .all()
    )

    evaluation_response = [
        EvaluationResponse(
            question=item.question,

            answer=item.answer,

            score=item.score,

            feedback=item.feedback,

            explanation=item.explanation,

            competency=item.competency,

            difficulty=item.difficulty
        )

        for item in evaluations
    ]

    scores = [
        item.score
        for item in evaluations
        if item.score is not None
    ]

    final_score = (
        sum(scores) / len(scores)
        if scores
        else 0
    )

    # --------------------------------------------------------
    # STORED BENCHMARK
    # --------------------------------------------------------

    readiness_metrics = (
        assessment.readiness_metrics or {}
    )

    improvement_gaps = (
        assessment.improvement_gaps or []
    )

    feedback = (
        assessment.feedback
        or "Assessment is still in progress."
    )

    semantic_similarity = 0.0

    # If the benchmark hasn't been generated yet,
    # return a sensible current-state result.
    if not readiness_metrics:

        candidate = (
            db.query(Candidate)
            .filter(
                Candidate.id
                == assessment.candidate_id
            )
            .first()
        )

        if candidate and assessment.target_role:

            try:

                benchmark = (
                    generate_readiness_benchmark(
                        candidate_id=assessment.candidate_id,

                        profile=(
                            candidate.resume_data or {}
                        ),

                        role_name=assessment.target_role,

                        evaluations=[
                            {
                                "question": item.question,

                                "answer": item.answer,

                                "score": item.score,

                                "feedback": item.feedback,

                                "explanation": item.explanation,

                                "competency": item.competency,

                                "difficulty": item.difficulty
                            }

                            for item in evaluations
                            if item.answer is not None
                        ]
                    )
                )

                readiness_metrics = (
                    benchmark["readiness_metrics"]
                )

                improvement_gaps = (
                    benchmark["improvement_gaps"]
                )

                feedback = benchmark["feedback"]

                semantic_similarity = (
                    benchmark["semantic_similarity"]
                )

            except Exception:
                pass

    overall_readiness = readiness_metrics.get(
        "overall_readiness",
        final_score * 10
    )

    return AssessmentResult(
        assessment_id=assessment.id,

        candidate_id=assessment.candidate_id,

        target_role=assessment.target_role,

        score=round(
            final_score,
            2
        ),

        technical_level=(
            assessment.technical_level
            or get_technical_level(
                final_score * 10
            )
        ),

        semantic_similarity=round(
            semantic_similarity,
            2
        ),

        readiness_metrics=readiness_metrics,

        improvement_gaps=improvement_gaps,

        feedback=feedback,

        evaluations=evaluation_response
    )