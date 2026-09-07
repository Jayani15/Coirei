from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from .database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=True)
    email = Column(String(150), nullable=True)

    # Complete structured candidate profile
    resume_data = Column(JSONB, nullable=False, default=dict)

    # Important fields detected as missing/weak
    missing_data = Column(JSONB, nullable=True, default=list)

    # Career preferences supplied by the candidate
    career_preferences = Column(JSONB, nullable=True, default=dict)

    # Roles selected by candidate
    preferred_roles = Column(JSONB, nullable=True, default=list)

    # 0 - 100
    profile_completeness = Column(Float, nullable=False, default=0)

    profile_status = Column(
        String(30),
        nullable=False,
        default="incomplete"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    assessments = relationship(
        "Assessment",
        back_populates="candidate",
        cascade="all, delete-orphan"
    )

    role_recommendations = relationship(
        "RoleRecommendation",
        back_populates="candidate",
        cascade="all, delete-orphan"
    )

    gap_conversations = relationship(
        "GapConversation",
        back_populates="candidate",
        cascade="all, delete-orphan"
    )


class RoleRecommendation(Base):
    __tablename__ = "role_recommendations"

    id = Column(Integer, primary_key=True, index=True)

    candidate_id = Column(
        Integer,
        ForeignKey("candidates.id"),
        nullable=False
    )

    role = Column(String(150), nullable=False)
    match_score = Column(Float, nullable=False)

    reason = Column(Text, nullable=True)

    missing_skills = Column(
        JSONB,
        nullable=True,
        default=list
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    candidate = relationship(
        "Candidate",
        back_populates="role_recommendations"
    )


class GapConversation(Base):
    __tablename__ = "gap_conversations"

    id = Column(Integer, primary_key=True, index=True)

    candidate_id = Column(
        Integer,
        ForeignKey("candidates.id"),
        nullable=False
    )

    field = Column(String(100), nullable=False)

    question = Column(Text, nullable=False)

    answer = Column(Text, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    candidate = relationship(
        "Candidate",
        back_populates="gap_conversations"
    )


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)

    candidate_id = Column(
        Integer,
        ForeignKey("candidates.id"),
        nullable=False
    )

    target_role = Column(
        String(150),
        nullable=True
    )

    score = Column(Float, nullable=True)

    feedback = Column(Text, nullable=True)

    technical_level = Column(
        String(50),
        nullable=True
    )

    readiness_metrics = Column(
        JSONB,
        nullable=True,
        default=dict
    )

    improvement_gaps = Column(
        JSONB,
        nullable=True,
        default=list
    )

    status = Column(
        String(30),
        nullable=False,
        default="in_progress"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    candidate = relationship(
        "Candidate",
        back_populates="assessments"
    )

    evaluations = relationship(
        "Evaluation",
        back_populates="assessment",
        cascade="all, delete-orphan"
    )


class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)

    assessment_id = Column(
        Integer,
        ForeignKey("assessments.id"),
        nullable=False
    )

    question = Column(Text, nullable=False)

    answer = Column(Text, nullable=True)

    explanation = Column(Text, nullable=True)

    feedback = Column(Text, nullable=True)

    score = Column(Float, nullable=True)

    competency = Column(
        String(100),
        nullable=True
    )

    difficulty = Column(
        String(30),
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    assessment = relationship(
        "Assessment",
        back_populates="evaluations"
    )