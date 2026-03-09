import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

TECH_SKILLS = {
    # Programming Languages
    "python", "java", "javascript",  "c++", "ruby", "go","rust", "swift", "kotlin", "r", "shell",
    # Web Technologies
    "html", "css", "react", "angular", "node", "express", "django", "flask", "fastapi", "spring", "next.js",
    # Databases
    "sql", "mysql", "postgresql", "mongodb","oracle", "sql server", "elasticsearch", "neo4j", "sqlite",
    # Cloud & DevOps
    "aws", "azure", "docker", "kubernetes", "jenkins", "ci/cd", "git", "github", "gitlab",
    # Data & AI
    "machine learning", "deep learning", "nlp", "computer vision", "tensorflow","pytorch", "scikit-learn", "pandas", "numpy", "tableau", "power bi", "data science", "statistics",
    # Other
    "rest api", "graphql",  "agile", "scrum", "linux", "unix", "windows", "networking", "security", "testing"
}


def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s.#+]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def extract_skills(text, skills):
    found = set()
    for s in skills:
        if re.search(r"\b" + re.escape(s) + r"\b", text):
            found.add(s)
    return list(found)

def extract_years(text):
    matches = re.findall(r"(\d+)\s*years?", text)
    return max([int(x) for x in matches], default=0)

def technical_match(job, resume):
    vec = TfidfVectorizer(stop_words="english")
    tfidf = vec.fit_transform([job, resume])
    sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]

    job_sk = extract_skills(job, TECH_SKILLS)
    res_sk = extract_skills(resume, TECH_SKILLS)

    skill_score = len(set(job_sk)&set(res_sk))/len(job_sk) if job_sk else 0

    return (sim*0.6 + skill_score*0.4)*100, job_sk, res_sk

