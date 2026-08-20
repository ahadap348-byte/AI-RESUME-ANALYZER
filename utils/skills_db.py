"""
Predefined skills taxonomy for multi-domain skill extraction.
"""

SKILLS_DB = {
    "Programming Languages": [
        "python", "java", "c++", "c#", "c", "javascript", "typescript", "ruby",
        "php", "swift", "kotlin", "go", "golang", "rust", "scala", "r", "dart", "shell", "bash"
    ],
    "Web & Frontend": [
        "html", "html5", "css", "css3", "sass", "bootstrap", "tailwind", "react",
        "react.js", "next.js", "vue", "vue.js", "angular", "svelte", "jquery",
        "redux", "webpack", "vite", "graphql", "rest api"
    ],
    "Backend & Frameworks": [
        "django", "flask", "fastapi", "spring", "spring boot", "express", "express.js",
        "node.js", "nestjs", "asp.net", "laravel", "rails", "ruby on rails"
    ],
    "Data Science & Machine Learning": [
        "machine learning", "deep learning", "nlp", "natural language processing",
        "computer vision", "tensorflow", "pytorch", "keras", "scikit-learn", "sklearn",
        "pandas", "numpy", "matplotlib", "seaborn", "scipy", "xgboost", "lightgbm",
        "hugging face", "transformers", "llm", "genai", "langchain", "llamaindex",
        "opencv", "bert", "gpt", "rag"
    ],
    "Databases & Big Data": [
        "sql", "mysql", "postgresql", "postgres", "mongodb", "sqlite", "redis",
        "cassandra", "elasticsearch", "neo4j", "firebase", "dynamodb", "snowflake",
        "bigquery", "spark", "apache spark", "hadoop", "kafka"
    ],
    "Cloud & DevOps": [
        "aws", "azure", "gcp", "google cloud", "docker", "kubernetes", "k8s",
        "jenkins", "gitlab ci", "github actions", "terraform", "ansible",
        "linux", "nginx", "apache", "prometheus", "grafana", "ci/cd"
    ],
    "Soft Skills & Management": [
        "leadership", "communication", "teamwork", "problem solving", "critical thinking",
        "project management", "agile", "scrum", "kanban", "time management",
        "collaboration", "mentoring", "client management", "negotiation"
    ]
}

# Flatten list for quick lookup
ALL_SKILLS = set()
for category, skill_list in SKILLS_DB.items():
    for skill in skill_list:
        ALL_SKILLS.add(skill.lower())
