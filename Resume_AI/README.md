# AI-Powered Candidate Intelligence & Job Readiness Platform

## Overview

This project is an AI-powered resume assessment and candidate intelligence system that analyzes a candidate's resume, identifies missing information, recommends suitable job roles, and evaluates technical readiness through an adaptive AI assessment.

The system goes beyond simple resume keyword matching by building a structured candidate profile from an unstructured resume and using AI to understand skills, education, experience, projects, career preferences, and role suitability.

It also uses a conversational approach to collect missing profile information and conducts a role-specific technical assessment where questions adapt based on the candidate's previous answers.

## Objectives

- Parse resumes automatically using AI.
- Extract structured candidate information from PDF resumes.
- Detect missing or incomplete profile information.
- Calculate candidate profile completeness.
- Generate AI questions to collect missing information.
- Recommend suitable job roles based on the candidate profile.
- Allow candidates to select preferred roles.
- Generate role-specific technical questions.
- Evaluate candidate answers using AI.
- Adapt subsequent assessment questions based on previous performance.
- Generate a final job-readiness benchmark.
- Identify areas where the candidate needs improvement.

## System Workflow

```text
Resume PDF
    |
    v
PDF Text Extraction
    |
    v
AI Resume Parsing
    |
    v
Structured Candidate Profile
    |
    +-------------------+
    |                   |
    v                   v
Missing Information   Profile Completeness
    |
    v
AI Gap Questions
    |
    v
Candidate Answers
    |
    v
Updated Candidate Profile
    |
    v
Role Recommendations
    |
    v
Preferred Role Selection
    |
    v
Adaptive AI Assessment
    |
    v
Answer Evaluation
    |
    v
Adaptive Next Question
    |
    v
Final Readiness Analysis
    |
    v
Readiness Metrics + Improvement Gaps
```

## Key Features

### 1. AI Resume Parsing

The candidate uploads a PDF resume. PyMuPDF is used to extract the text, which is then processed by the AI system.

The system extracts structured information such as:

- Name
- Email
- Education
- Skills
- Experience
- Projects
- Certifications
- Training
- Achievements
- Career preferences

This structured information is stored as the candidate profile.

### 2. Profile Completeness and Gap Detection

The system checks the candidate profile and identifies missing information.

For example:

```text
Skills          -> Present
Education       -> Present
Projects        -> Present
Certifications  -> Missing
Training        -> Missing
Achievements    -> Missing
```

A profile completeness score is calculated so that the candidate can see how complete their profile is.

### 3. Conversational Profile Completion

Instead of requiring the candidate to manually fill every missing field, the AI generates questions based on the missing information.

Example:

```text
AI:
What certifications have you completed?

Candidate:
I completed a professional data analytics certification.

        |
        v

Candidate profile is updated
        |
        v

Completeness is recalculated
        |
        v

AI asks the next relevant question
```

### 4. AI-Based Role Recommendation

The system analyzes the candidate profile and recommends suitable job roles.

Each recommendation can contain:

- Role
- Match score
- Reason for recommendation
- Missing skills

This gives the candidate both a recommendation and an explanation of why the role is suitable.

### 5. Preferred Role Selection

The candidate can select preferred roles from the available recommendations.

The selected role is stored in the database and is used to personalize the technical assessment.

### 6. Adaptive Technical Assessment

The assessment is role-specific rather than using the same fixed questions for every candidate.

For example, an AI Engineer assessment can evaluate areas such as:

- Machine Learning
- Deep Learning
- Python
- AI concepts
- Model evaluation
- Practical implementation

The system keeps track of previous questions and answers so that the assessment can adapt to the candidate.

### 7. AI Answer Evaluation

Each submitted answer is evaluated by the AI system.

The evaluation includes:

- Score
- Feedback
- Explanation
- Competency
- Difficulty

The candidate therefore receives more than just a numerical score.

### 8. Adaptive Question Generation

The next question is generated using the candidate's previous assessment performance.

This allows the assessment to focus on the candidate's demonstrated strengths and weaknesses instead of simply following a fixed question sequence.

The current implementation evaluates up to 5 questions before producing the final assessment result.

### 9. Job-Readiness Benchmark

After the assessment is completed, the system generates a final readiness analysis.

The result can include metrics for areas such as:

- Technical fundamentals
- Role-specific knowledge
- Practical implementation
- Problem solving
- Project depth
- Conceptual clarity
- Overall readiness

The system also provides improvement gaps to help identify areas that the candidate should work on.

## Technology Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic

### AI / NLP

A Large Language Model is used for:

- Resume parsing
- Profile analysis
- Gap-question generation
- Profile updating
- Role recommendation
- Technical question generation
- Answer evaluation
- Readiness analysis

### Resume Processing

- PyMuPDF (`fitz`) is used to extract text from PDF resumes.

### Vector Database / Semantic Retrieval

- Qdrant is used for storing candidate profile information and supporting semantic retrieval.

### Configuration

- `python-dotenv` is used to load environment variables from the `.env` file.

### API Documentation and Testing

FastAPI provides an interactive Swagger UI for testing the backend endpoints.

## Project Structure

```text
Resume_AI/
|
+-- app/
|   +-- ai.py
|   +-- database.py
|   +-- main.py
|   +-- models.py
|   +-- parser.py
|   +-- routes.py
|   +-- schemas.py
|   +-- vector_db.py
|   +-- roles.py
|
+-- uploads/
|
+-- .env
+-- requirements.txt
+-- README.md
```

## Database Design

The application uses PostgreSQL for persistent storage.

### Candidate

Stores the candidate's main profile and resume information.

```text
candidates
|
+-- id
+-- name
+-- email
+-- resume_data
+-- missing_data
+-- career_preferences
+-- preferred_roles
+-- profile_completeness
+-- profile_status
+-- created_at
```

### Assessment

Stores the candidate's assessment information.

```text
assessments
|
+-- id
+-- candidate_id
+-- target_role
+-- score
+-- technical_level
+-- feedback
+-- readiness_metrics
+-- improvement_gaps
+-- status
+-- created_at
```

### Evaluation

Stores individual assessment questions and their evaluations.

```text
evaluations
|
+-- id
+-- assessment_id
+-- question
+-- answer
+-- explanation
+-- feedback
+-- score
+-- competency
+-- difficulty
+-- created_at
```

### Gap Conversation

Stores the questions asked to complete missing candidate information and the candidate's answers.

### Role Recommendation

Stores AI-generated role recommendations and their matching information.

## API Endpoints

The main API flow is exposed through FastAPI.

### Resume

```text
POST /api/resume/upload
```

Uploads and processes a resume.

### Candidate Profile

```text
GET /api/candidate/{candidate_id}
```

Returns the candidate profile.

### Gap Detection and Profile Completion

```text
GET  /api/candidate/{candidate_id}/gap-question
POST /api/candidate/{candidate_id}/gap-answer
```

Generates questions for missing information and updates the candidate profile with the answers.

### Role Recommendations

```text
GET /api/candidate/{candidate_id}/recommendations
```

Generates suitable job-role recommendations.

### Role Selection

```text
POST /api/candidate/{candidate_id}/roles
```

Stores the candidate's preferred roles.

### Assessment

```text
POST /api/assessment/start/{candidate_id}
POST /api/assessment/{assessment_id}/answer
GET  /api/assessment/{assessment_id}/result
```

These endpoints start the assessment, evaluate answers, generate adaptive questions, and return the final readiness result.

## Installation and Setup

### 1. Clone or open the project

Open the project directory in your terminal or IDE.

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root and configure the required values.

Example:

```env
DATABASE_URL=your_postgresql_database_url
OPENAI_API_KEY=your_ai_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
```

Use the actual environment variable names required by the project's `ai.py` and `vector_db.py`.

### 5. Start the backend

```bash
uvicorn app.main:app --reload
```

The API will run locally.

### 6. Open Swagger UI

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger UI can be used to test all available API endpoints.

## Testing

The complete tested flow is:

```text
1. Upload Resume
       |
2. Retrieve Candidate Profile
       |
3. Generate Gap Question
       |
4. Submit Gap Answer
       |
5. Verify Profile Update
       |
6. Generate Role Recommendations
       |
7. Select Preferred Role
       |
8. Start Assessment
       |
9. Submit Assessment Answers
       |
10. Verify Adaptive Questions
       |
11. Complete Assessment
       |
12. Retrieve Final Readiness Result
```

Important validation points include:

- Resume data is successfully extracted.
- Missing profile information is detected.
- Candidate answers update the profile.
- Profile completeness is recalculated.
- Suitable roles are recommended.
- Selected roles are stored.
- Assessment questions are generated for the selected role.
- Answers receive AI-generated scores and feedback.
- Subsequent questions are generated adaptively.
- The final assessment contains readiness metrics and improvement gaps.

## Example End-to-End Flow

```text
Candidate uploads resume
          |
          v
AI extracts candidate information
          |
          v
System detects missing information
          |
          v
AI asks targeted questions
          |
          v
Candidate provides additional information
          |
          v
Candidate profile becomes more complete
          |
          v
AI recommends suitable job roles
          |
          v
Candidate selects a preferred role
          |
          v
AI generates role-specific assessment
          |
          v
Candidate answers technical questions
          |
          v
AI evaluates each answer
          |
          v
Assessment adapts to previous answers
          |
          v
Final readiness benchmark is generated
```

## Why This Project Is Different

Traditional resume screening systems generally focus on extracting keywords, matching resumes to job descriptions, or calculating a simple similarity score.

This project follows a broader candidate-intelligence approach:

```text
Resume
  |
  +--> Structured Profile
  |
  +--> Missing Information
  |
  +--> Conversational Profile Completion
  |
  +--> Career Role Recommendations
  |
  +--> Role-Specific Assessment
  |
  +--> Adaptive Evaluation
  |
  +--> Job-Readiness Benchmark
```

Therefore, the system does not stop at **"What is present in the resume?"**

It also attempts to answer:

- What information is missing?
- What roles could suit the candidate?
- What technical skills does the candidate demonstrate?
- How well does the candidate perform in a role-specific assessment?
- What areas should the candidate improve?
- How ready is the candidate for the selected role?

## Future Enhancements

Possible future improvements include:

- Frontend dashboard for candidates.
- Recruiter dashboard.
- Support for DOCX resumes.
- More sophisticated semantic candidate-job matching.
- More detailed competency tracking.
- Difficulty adjustment based on answer performance.
- Interview simulation.
- Personalized learning recommendations.
- Job-description analysis.
- Candidate-to-job ranking.
- Advanced analytics and visualizations.

## Conclusion

The AI-Powered Candidate Intelligence & Job Readiness Platform combines **resume intelligence, conversational profile completion, semantic role recommendation, adaptive technical assessment, and readiness benchmarking** into a single system.

The overall goal is to move from traditional resume screening toward a more comprehensive system that understands a candidate's profile, evaluates their demonstrated abilities, identifies gaps, and provides actionable information about their readiness for potential career roles.
