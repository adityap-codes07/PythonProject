import streamlit as st
import pandas as pd
import numpy as np
import re
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
import plotly.graph_objects as go
import plotly.express as px

# ======================================================
# ADVANCED CONFIG
# ======================================================
st.set_page_config(
    page_title="AI Resume Analyzer Pro",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ======================================================
# PREMIUM STYLING
# ======================================================
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        * {
            font-family: 'Inter', sans-serif;
        }

        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}

        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        }

        .block-container {
            padding: 2rem 3rem;
            max-width: 1400px;
        }

        .stButton>button {
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            color: white;
            border: none;
            padding: 0.75rem 2rem;
            font-size: 1.05rem;
            font-weight: 600;
            border-radius: 12px;
            box-shadow: 0 8px 20px rgba(99, 102, 241, 0.4);
            transition: all 0.3s ease;
        }

        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 28px rgba(99, 102, 241, 0.5);
        }

        .stTextInput>div>div>input,
        .stTextArea>div>div>textarea {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(100, 116, 139, 0.3);
            border-radius: 10px;
            color: #e2e8f0;
            padding: 0.75rem;
            font-size: 0.95rem;
        }

        .stTextInput>div>div>input:focus,
        .stTextArea>div>div>textarea:focus {
            border-color: #6366f1;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        }

        div[data-testid="stDataFrame"] {
            background: rgba(15, 23, 42, 0.4);
            border-radius: 12px;
            padding: 1rem;
        }

        .metric-card {
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.8) 0%, rgba(30, 41, 59, 0.8) 100%);
            border: 1px solid rgba(100, 116, 139, 0.2);
            border-radius: 16px;
            padding: 1.8rem;
            text-align: center;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
            transition: transform 0.3s ease;
        }

        .metric-card:hover {
            transform: translateY(-5px);
        }

        .skill-badge {
            display: inline-block;
            background: rgba(99, 102, 241, 0.15);
            border: 1px solid rgba(99, 102, 241, 0.3);
            color: #a5b4fc;
            padding: 0.4rem 0.9rem;
            border-radius: 20px;
            margin: 0.3rem;
            font-size: 0.85rem;
            font-weight: 500;
        }

        .gap-badge {
            display: inline-block;
            background: rgba(239, 68, 68, 0.15);
            border: 1px solid rgba(239, 68, 68, 0.3);
            color: #fca5a5;
            padding: 0.4rem 0.9rem;
            border-radius: 20px;
            margin: 0.3rem;
            font-size: 0.85rem;
            font-weight: 500;
        }
    </style>
""", unsafe_allow_html=True)

# ======================================================
# ENHANCED NLP & SKILL EXTRACTION
# ======================================================

TECH_SKILLS = {
    # Programming Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "ruby", "go",
    "rust", "swift", "kotlin", "scala", "r", "php", "perl", "bash", "shell",

    # Web Technologies
    "html", "css", "react", "angular", "vue", "node", "express", "django",
    "flask", "fastapi", "spring", "asp.net", "laravel", "rails", "next.js",

    # Databases
    "sql", "mysql", "postgresql", "mongodb", "redis", "cassandra", "dynamodb",
    "oracle", "sql server", "elasticsearch", "neo4j", "sqlite",

    # Cloud & DevOps
    "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "ci/cd",
    "terraform", "ansible", "git", "github", "gitlab", "circleci",

    # Data & AI
    "machine learning", "deep learning", "nlp", "computer vision", "tensorflow",
    "pytorch", "scikit-learn", "pandas", "numpy", "spark", "hadoop", "kafka",
    "airflow", "tableau", "power bi", "data science", "statistics",

    # Other
    "rest api", "graphql", "microservices", "agile", "scrum", "jira",
    "linux", "unix", "windows", "networking", "security", "testing"
}

COMMUNICATION_SKILLS = [
    "communication", "presentation", "documentation", "technical writing",
    "stakeholder management", "client interaction", "verbal", "written",
    "public speaking", "reporting", "collaboration", "cross-functional"
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


def clean_text(text):
    """Advanced text preprocessing"""
    text = text.lower()
    text = re.sub(r'[^\w\s.#+]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_skills(text, skill_set):
    """Extract skills with better matching"""
    text_lower = text.lower()
    found_skills = set()

    for skill in skill_set:
        # Use word boundaries for better matching
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.add(skill)

    return list(found_skills)


def extract_years_of_experience(text):
    """Extract years of experience from resume"""
    patterns = [
        r'(\d+)\+?\s*years?\s+(?:of\s+)?experience',
        r'experience\s*:?\s*(\d+)\+?\s*years?',
        r'(\d+)\+?\s*yrs?'
    ]

    years = []
    for pattern in patterns:
        matches = re.findall(pattern, text.lower())
        years.extend([int(m) for m in matches])

    return max(years) if years else 0


def advanced_technical_matching(job_text, resume_text):
    """Multi-strategy technical skill matching"""
    # Strategy 1: TF-IDF Cosine Similarity
    vectorizer = TfidfVectorizer(
        stop_words='english',
        ngram_range=(1, 3),
        max_features=500
    )
    tfidf = vectorizer.fit_transform([job_text, resume_text])
    tfidf_score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]

    # Strategy 2: Skill-based matching
    job_skills = extract_skills(job_text, TECH_SKILLS)
    resume_skills = extract_skills(resume_text, TECH_SKILLS)

    if job_skills:
        skill_match = len(set(job_skills) & set(resume_skills)) / len(job_skills)
    else:
        skill_match = 0

    # Weighted combination
    final_score = (tfidf_score * 0.6 + skill_match * 0.4) * 100

    return final_score, job_skills, resume_skills


def create_gauge_chart(score, title, color):
    """Create beautiful gauge chart"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 16, 'color': '#e2e8f0'}},
        number={'font': {'size': 40, 'color': color}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#475569"},
            'bar': {'color': color},
            'bgcolor': "rgba(15, 23, 42, 0.4)",
            'borderwidth': 2,
            'bordercolor': "#475569",
            'steps': [
                {'range': [0, 50], 'color': 'rgba(239, 68, 68, 0.2)'},
                {'range': [50, 75], 'color': 'rgba(234, 179, 8, 0.2)'},
                {'range': [75, 100], 'color': 'rgba(34, 197, 94, 0.2)'}
            ],
        }
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "#e2e8f0"},
        height=250,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    return fig


def section_header(title, emoji):
    """Premium section headers"""
    st.markdown(f"""
    <div style="
        margin: 2.5rem 0 1.5rem 0;
        padding: 1rem 1.5rem;
        background: linear-gradient(90deg, rgba(99, 102, 241, 0.15) 0%, transparent 100%);
        border-left: 4px solid #6366f1;
        border-radius: 8px;
    ">
        <h2 style="
            color: #e2e8f0;
            margin: 0;
            font-size: 1.5rem;
            font-weight: 600;
        ">
            {emoji} {title}
        </h2>
    </div>
    """, unsafe_allow_html=True)


# ======================================================
# HERO HEADER
# ======================================================
st.markdown("""
<div style="
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
    border: 1px solid rgba(99, 102, 241, 0.3);
    padding: 3rem 2.5rem;
    border-radius: 20px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
    margin-bottom: 3rem;
    text-align: center;
">
    <h1 style="
        color: #f8fafc;
        margin-bottom: 1rem;
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    ">
        🚀 AI-Powered Resume Intelligence Platform
    </h1>
    <p style="
        color: #cbd5e1;
        font-size: 1.15rem;
        max-width: 900px;
        margin: 0 auto;
        line-height: 1.6;
    ">
        Advanced ATS simulation with multi-dimensional analysis, real-time skill gap detection,
        and actionable career insights powered by enterprise-grade NLP algorithms.
    </p>
</div>
""", unsafe_allow_html=True)

# ======================================================
# INPUT SECTION
# ======================================================
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    section_header("Job Requirements", "📋")
    job_role = st.text_input("Position Title", placeholder="e.g., Senior Software Engineer")
    job_description = st.text_area(
        "Complete Job Description",
        height=300,
        placeholder="Paste the full job description including required skills, responsibilities, qualifications, and experience..."
    )

with col2:
    section_header("Candidate Profile", "👤")
    candidate_name = st.text_input("Candidate Name (Optional)", placeholder="John Doe")
    resume_text = st.text_area(
        "Complete Resume Content",
        height=300,
        placeholder="Paste your entire resume including professional summary, work experience, education, skills, projects, and achievements..."
    )

# ======================================================
# ANALYSIS ENGINE
# ======================================================
st.markdown("<br>", unsafe_allow_html=True)

if st.button("🔬 Run Advanced Analysis", use_container_width=True):

    if not job_description or not resume_text:
        st.error("⚠️ Please provide both job description and resume content.")
    else:
        with st.spinner("🔄 Analyzing resume with AI models..."):
            # Clean text
            job_clean = clean_text(job_description)
            resume_clean = clean_text(resume_text)

            # ===== TECHNICAL SKILLS ANALYSIS =====
            tech_score, job_skills, resume_skills = advanced_technical_matching(job_clean, resume_clean)
            matched_skills = list(set(job_skills) & set(resume_skills))
            missing_skills = list(set(job_skills) - set(resume_skills))

            # ===== COMMUNICATION ANALYSIS =====
            comm_found = extract_skills(resume_clean, COMMUNICATION_SKILLS)
            comm_score = min((len(comm_found) / max(len(COMMUNICATION_SKILLS), 1)) * 100, 100)

            # ===== SOFT SKILLS ANALYSIS =====
            soft_found = extract_skills(resume_clean, SOFT_SKILLS)
            soft_score = min((len(soft_found) / max(len(SOFT_SKILLS), 1)) * 100, 100)

            # ===== EXPERIENCE ANALYSIS =====
            exp_found = extract_skills(resume_clean, EXPERIENCE_KEYWORDS)
            years_exp = extract_years_of_experience(resume_clean)
            exp_score = min((len(exp_found) / 8) * 100 + (years_exp * 5), 100)

            # ===== WEIGHTED FINAL SCORE =====
            final_score = (
                    tech_score * WEIGHTS["technical"] +
                    comm_score * WEIGHTS["communication"] +
                    soft_score * WEIGHTS["soft_skills"] +
                    exp_score * WEIGHTS["experience"]
            )

            # Determine fit level
            if final_score >= 80:
                fit_level = "Excellent"
                fit_color = "#22c55e"
            elif final_score >= 65:
                fit_level = "Good"
                fit_color = "#eab308"
            elif final_score >= 50:
                fit_level = "Moderate"
                fit_color = "#f97316"
            else:
                fit_level = "Needs Improvement"
                fit_color = "#ef4444"

        # ======================================================
        # RESULTS DASHBOARD
        # ======================================================
        st.markdown("<br>", unsafe_allow_html=True)
        section_header("Analysis Results", "📊")

        # Main Score Cards
        st.markdown(f"""
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; margin: 2rem 0;">
            <div class="metric-card">
                <div style="font-size: 3rem; font-weight: 700; color: {fit_color}; margin-bottom: 0.5rem;">
                    {final_score:.1f}
                </div>
                <div style="color: #94a3b8; font-size: 0.95rem; text-transform: uppercase; letter-spacing: 1px;">
                    Overall ATS Score
                </div>
            </div>
            <div class="metric-card">
                <div style="font-size: 3rem; font-weight: 700; color: #60a5fa; margin-bottom: 0.5rem;">
                    {tech_score:.1f}%
                </div>
                <div style="color: #94a3b8; font-size: 0.95rem; text-transform: uppercase; letter-spacing: 1px;">
                    Technical Match
                </div>
            </div>
            <div class="metric-card">
                <div style="font-size: 2.2rem; font-weight: 700; color: {fit_color}; margin-bottom: 0.5rem;">
                    {fit_level}
                </div>
                <div style="color: #94a3b8; font-size: 0.95rem; text-transform: uppercase; letter-spacing: 1px;">
                    Candidate Fit
                </div>
            </div>
            <div class="metric-card">
                <div style="font-size: 3rem; font-weight: 700; color: #a78bfa; margin-bottom: 0.5rem;">
                    {len(matched_skills)}
                </div>
                <div style="color: #94a3b8; font-size: 0.95rem; text-transform: uppercase; letter-spacing: 1px;">
                    Skills Matched
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Gauge Charts
        section_header("Detailed Scoring Breakdown", "📈")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.plotly_chart(
                create_gauge_chart(tech_score, "Technical", "#60a5fa"),
                use_container_width=True
            )

        with col2:
            st.plotly_chart(
                create_gauge_chart(comm_score, "Communication", "#34d399"),
                use_container_width=True
            )

        with col3:
            st.plotly_chart(
                create_gauge_chart(soft_score, "Soft Skills", "#fbbf24"),
                use_container_width=True
            )

        with col4:
            st.plotly_chart(
                create_gauge_chart(exp_score, "Experience", "#a78bfa"),
                use_container_width=True
            )

        # Detailed Table
        section_header("Category Breakdown", "📋")

        df = pd.DataFrame({
            "Category": ["Technical Skills", "Communication", "Soft Skills", "Experience"],
            "Score": [f"{tech_score:.1f}%", f"{comm_score:.1f}%", f"{soft_score:.1f}%", f"{exp_score:.1f}%"],
            "Weight": ["45%", "20%", "20%", "15%"],
            "Impact": [
                f"{tech_score * WEIGHTS['technical']:.1f}",
                f"{comm_score * WEIGHTS['communication']:.1f}",
                f"{soft_score * WEIGHTS['soft_skills']:.1f}",
                f"{exp_score * WEIGHTS['experience']:.1f}"
            ]
        })

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        # Skills Analysis
        section_header("Skills Intelligence", "🎯")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**✅ Matched Skills**")
            if matched_skills:
                skills_html = "".join([f'<span class="skill-badge">{skill}</span>' for skill in matched_skills[:15]])
                st.markdown(skills_html, unsafe_allow_html=True)
            else:
                st.info("No direct skill matches detected.")

        with col2:
            st.markdown("**⚠️ Missing Skills (Top Priority)**")
            if missing_skills:
                gaps_html = "".join([f'<span class="gap-badge">{skill}</span>' for skill in missing_skills[:15]])
                st.markdown(gaps_html, unsafe_allow_html=True)
            else:
                st.success("All key skills covered!")

        # Recommendations
        section_header("AI-Powered Recommendations", "💡")

        recommendations = []

        if tech_score < 70:
            recommendations.append({
                "priority": "🔴 High",
                "category": "Technical Skills",
                "action": f"Acquire {len(missing_skills)} missing technical skills: {', '.join(missing_skills[:5])}{'...' if len(missing_skills) > 5 else ''}",
                "impact": "Will increase overall score by ~15-20 points"
            })

        if comm_score < 60:
            recommendations.append({
                "priority": "🟡 Medium",
                "category": "Communication",
                "action": "Add examples of presentations, documentation, and stakeholder interactions to resume",
                "impact": "Will improve overall score by ~8-12 points"
            })

        if soft_score < 60:
            recommendations.append({
                "priority": "🟡 Medium",
                "category": "Soft Skills",
                "action": "Highlight leadership, teamwork, and problem-solving achievements with quantifiable results",
                "impact": "Will improve overall score by ~8-12 points"
            })

        if exp_score < 50:
            recommendations.append({
                "priority": "🟠 Medium-High",
                "category": "Experience",
                "action": "Add more project details, internships, or freelance work. Quantify achievements (e.g., 'increased efficiency by 30%')",
                "impact": "Will improve overall score by ~6-10 points"
            })

        if final_score >= 80:
            st.success(
                "🎉 **Outstanding Match!** Your resume is highly competitive for this role. Consider applying immediately.")
        elif recommendations:
            for rec in recommendations:
                st.warning(f"""
**{rec['priority']} - {rec['category']}**  
📌 {rec['action']}  
💫 *{rec['impact']}*
                """)
        else:
            st.info(
                "✨ Your resume is well-aligned with the job requirements. Minor optimizations may further enhance your chances.")

        # Footer
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="
            text-align: center;
            padding: 1.5rem;
            background: rgba(15, 23, 42, 0.4);
            border-radius: 12px;
            border: 1px solid rgba(100, 116, 139, 0.2);
        ">
            <p style="color: #94a3b8; margin: 0; font-size: 0.9rem;">
                Analysis completed on {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}
                {'for ' + candidate_name if candidate_name else ''} | Powered by Advanced NLP & ML Models
            </p>
        </div>
        """, unsafe_allow_html=True)