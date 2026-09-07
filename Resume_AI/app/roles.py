ROLE_PROFILES = {
    "AI Engineer": {
        "skills": [
            "Python",
            "Machine Learning",
            "Deep Learning",
            "NLP",
            "LLM",
            "RAG",
            "FastAPI",
            "Vector Database"
        ],
        "competencies": [
            "machine learning",
            "deep learning",
            "LLM application development",
            "RAG systems",
            "API development",
            "problem solving"
        ]
    },

    "Machine Learning Engineer": {
        "skills": [
            "Python",
            "Machine Learning",
            "Deep Learning",
            "Scikit-learn",
            "TensorFlow",
            "PyTorch",
            "SQL",
            "Model Deployment"
        ],
        "competencies": [
            "data preprocessing",
            "machine learning",
            "model evaluation",
            "deep learning",
            "deployment",
            "problem solving"
        ]
    },

    "Data Scientist": {
        "skills": [
            "Python",
            "SQL",
            "Statistics",
            "Machine Learning",
            "Pandas",
            "NumPy",
            "Data Visualization"
        ],
        "competencies": [
            "statistics",
            "data analysis",
            "machine learning",
            "experimentation",
            "problem solving"
        ]
    },

    "Backend Developer": {
        "skills": [
            "Python",
            "FastAPI",
            "REST APIs",
            "PostgreSQL",
            "SQL",
            "Docker",
            "Authentication",
            "System Design"
        ],
        "competencies": [
            "API development",
            "database design",
            "authentication",
            "backend architecture",
            "system design",
            "problem solving"
        ]
    },

    "Full Stack Developer": {
        "skills": [
            "Python",
            "JavaScript",
            "React",
            "HTML",
            "CSS",
            "REST APIs",
            "PostgreSQL",
            "Git"
        ],
        "competencies": [
            "frontend development",
            "backend development",
            "API integration",
            "database management",
            "problem solving"
        ]
    },

    "Data Analyst": {
        "skills": [
            "Python",
            "SQL",
            "Excel",
            "Pandas",
            "NumPy",
            "Power BI",
            "Tableau",
            "Statistics"
        ],
        "competencies": [
            "data cleaning",
            "data analysis",
            "SQL querying",
            "visualization",
            "statistics",
            "business problem solving"
        ]
    }
}


def get_role(role_name: str):
    return ROLE_PROFILES.get(role_name)


def get_all_roles():
    return list(ROLE_PROFILES.keys())