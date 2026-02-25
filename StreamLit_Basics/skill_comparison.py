import streamlit as st
import pandas as pd
import re
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import plotly.graph_objects as go

st.set_page_config(page_title="Resume Analyzer", layout="wide")

st.title("ML Resume Analyzer")

# ================= SKILLS =================

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

COMMUNICATION_SKILLS = [
    "communication", "presentation", "documentation", "technical writing","client interaction", "verbal", "written","public speaking", "reporting", "collaboration"
]

SOFT_SKILLS = [
    "leadership", "teamwork", "problem solving", "analytical", "critical thinking",
    "time management", "adaptability", "creativity", "innovation", "mentoring",
    "strategic thinking", "decision making", "conflict resolution", "empathy"
]

EXPERIENCE_KEYWORDS = [
    "years", "experience", "worked", "developed", "led", "managed", "designed",
    "implemented", "built", "created", "delivered", "project", "internship",
    "contributed", "achieved", "improved", "optimized", "scaled"
]

# Industry-specific weights
WEIGHTS = {
    "technical": 0.45,
    "communication": 0.20,
    "soft_skills": 0.20,
    "experience": 0.15
}

# ================= HELPERS =================

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

def gauge(val, title):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=val,
        title={'text': title},
        gauge={'axis': {'range':[0,100]}}
    ))
    return fig

# ================= INPUT =================

col1,col2 = st.columns(2)

with col1:
    job_desc = st.text_area("Job Description", height=300)

with col2:
    resume = st.text_area("Resume", height=300)

# ================= ANALYSIS =================

if st.button("Run Analysis"):

    if not job_desc or not resume:
        st.error("Please provide both inputs.")
        st.stop()

    job = clean_text(job_desc)
    res = clean_text(resume)

    tech, job_sk, res_sk = technical_match(job,res)

    comm = len(extract_skills(res,COMMUNICATION_SKILLS))/len(COMMUNICATION_SKILLS)*100
    soft = len(extract_skills(res,SOFT_SKILLS))/len(SOFT_SKILLS)*100

    exp = len(extract_skills(res,EXPERIENCE_KEYWORDS))*15 + extract_years(res)*5
    exp = min(exp,100)

    final = (
        tech*WEIGHTS["technical"] +
        comm*WEIGHTS["communication"] +
        soft*WEIGHTS["soft_skills"] +
        exp*WEIGHTS["experience"]
    )

    st.subheader("Results")

    st.metric("Final ATS Score", round(final,1))
    st.metric("Technical Match", round(tech,1))

    c1,c2,c3,c4 = st.columns(4)

    c1.plotly_chart(gauge(tech,"Technical"),use_container_width=True)
    c2.plotly_chart(gauge(comm,"Communication"),use_container_width=True)
    c3.plotly_chart(gauge(soft,"Soft Skills"),use_container_width=True)
    c4.plotly_chart(gauge(exp,"Experience"),use_container_width=True)

    matched = list(set(job_sk)&set(res_sk))
    missing = list(set(job_sk)-set(res_sk))

    st.subheader("Matched Skills")
    st.write(matched)

    st.subheader("Missing Skills")
    st.write(missing)

    df = pd.DataFrame({
        "Category":["Technical","Communication","Soft","Experience"],
        "Score":[tech,comm,soft,exp]
    })

    st.dataframe(df)

    if final >= 80:
        st.success("Excellent fit")
    elif final >= 60:
        st.warning("Good fit")
    else:
        st.error("Needs improvement")

    st.caption(f"Completed on {datetime.now()}")
