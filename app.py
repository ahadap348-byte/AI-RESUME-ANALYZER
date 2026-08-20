"""
AI Resume Analyzer & Job Matcher
Streamlit Web Application
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.extractor import extract_text
from utils.nlp_parser import extract_contact_info, extract_skills
from utils.scorer import calculate_ats_score, match_resume_with_job
from utils.classifier import classifier
from utils.gemini_advisor import get_ai_feedback

# Page Configuration
st.set_page_config(
    page_title="AI Resume Analyzer & Job Matcher",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.3rem;
        font-weight: 700;
        background: linear-gradient(90deg, #3B82F6 0%, #8B5CF6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        color: #64748B;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    .skill-tag {
        display: inline-block;
        background: #3B82F622;
        color: #60A5FA;
        border: 1px solid #3B82F666;
        border-radius: 6px;
        padding: 4px 10px;
        margin: 3px;
        font-size: 0.85rem;
        font-weight: 500;
    }
    .missing-tag {
        display: inline-block;
        background: #EF444422;
        color: #F87171;
        border: 1px solid #EF444466;
        border-radius: 6px;
        padding: 4px 10px;
        margin: 3px;
        font-size: 0.85rem;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Setup
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=70)
    st.title("Settings & Tools")

    st.markdown("### 🤖 Optional GenAI Advisor")
    gemini_key = st.text_input("Gemini API Key", type="password", help="Optional: Enter key to unlock LLM deep feedback.")

    st.markdown("---")
    st.markdown("### 📋 Sample Profiles")
    load_sample = st.button("Load Sample Resume & JD")

    st.markdown("---")
    st.info("💡 **Tech Stack**: NLP (spaCy / NLTK / Regex), Scikit-Learn (TF-IDF & Naive Bayes), Streamlit, Plotly.")

# Default Sample Data
SAMPLE_RESUME = """ALEXANDER MORGAN
alex.morgan@email.com | +1 (555) 349-2041 | San Francisco, CA
linkedin.com/in/alexmorgan | github.com/alexmorgan

SUMMARY
Results-driven Senior Data Scientist with 5+ years of experience designing machine learning architectures, statistical models, and production NLP systems. Spearheaded real-time recommendation engines increasing customer engagement by 32%.

TECHNICAL SKILLS
- Languages: Python, SQL, R, Bash
- Frameworks & Libraries: PyTorch, TensorFlow, Scikit-Learn, Pandas, NumPy, Hugging Face, OpenCV
- Big Data & Cloud: AWS, Docker, Kubernetes, Spark, BigQuery, PostgreSQL
- Specialties: Natural Language Processing (NLP), Computer Vision, MLOps, CI/CD

PROFESSIONAL EXPERIENCE
Senior Data Scientist | Apex Analytics Inc. | 2021 - Present
- Architected and deployed an end-to-end NLP document classification pipeline processing 150K+ daily documents, reducing operational latency by 45%.
- Led a team of 4 engineers to train transformer models (BERT), achieving 94.2% accuracy.
- Automated feature store workflows using Apache Spark and AWS SageMaker.

Machine Learning Engineer | DataFlow Systems | 2019 - 2021
- Developed predictive churn models for 500K+ users with XGBoost, reducing churn rate by 18%.
- Optimized inference latency of deep learning models by 3x using TensorRT.

EDUCATION
Master of Science in Computer Science | Stanford University
Bachelor of Technology in Information Technology | University of California, Berkeley
"""

SAMPLE_JD = """Senior Machine Learning Engineer / Data Scientist

We are seeking an experienced ML Engineer to build scalable deep learning and NLP solutions.

Requirements:
- Strong proficiency in Python, PyTorch, Scikit-Learn, and SQL.
- Deep expertise in NLP, Transformers, LLMs, and RAG systems.
- Experience with Cloud platforms (AWS or GCP), Docker, Kubernetes, and Spark.
- Proven track record of deploying machine learning models into high-scale production.
- Excellent problem-solving and communication skills.
"""

# App Header
st.markdown('<div class="main-header">🎯 AI Resume Analyzer & Job Matcher</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Automated ATS scoring, NLP skill extraction, ML domain classification, and job matching.</div>', unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Single Resume Analysis",
    "💼 Job Description Matcher",
    "📂 Batch Resume Ranker",
    "🧠 ML Domain Classifier"
])

# --- TAB 1: Single Resume Analysis ---
with tab1:
    col_upload, col_preview = st.columns([1, 1])

    with col_upload:
        uploaded_file = st.file_uploader("Upload Resume (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"], key="single_resume")
        resume_text_area = SAMPLE_RESUME if load_sample else ""
        raw_text = extract_text(uploaded_file) if uploaded_file else resume_text_area
        resume_input = st.text_area("Or Paste Resume Text Here:", value=raw_text, height=260)

    if resume_input.strip():
        # Parsing & Analysis
        contact = extract_contact_info(resume_input)
        skills = extract_skills(resume_input)
        ats_results = calculate_ats_score(resume_input)

        with col_preview:
            st.markdown("### 👤 Candidate Profile")
            st.markdown(f"**Name:** {contact['name']}")
            st.markdown(f"**Email:** {contact['email']} | **Phone:** {contact['phone']}")
            st.markdown(f"**LinkedIn:** {contact['linkedin']} | **GitHub:** {contact['github']}")

            # ATS Gauge Chart
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=ats_results["total_score"],
                title={'text': "ATS Health Score", 'font': {'size': 20}},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#3B82F6"},
                    'steps': [
                        {'range': [0, 50], 'color': "#EF444422"},
                        {'range': [50, 75], 'color': "#F59E0B22"},
                        {'range': [75, 100], 'color': "#10B98122"}
                    ],
                    'threshold': {
                        'line': {'color': "white", 'width': 3},
                        'thickness': 0.75,
                        'value': ats_results["total_score"]
                    }
                }
            ))
            fig_gauge.update_layout(height=240, margin=dict(l=20, r=20, t=30, b=20), paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
            st.plotly_chart(fig_gauge, use_container_width=True)

        st.markdown("---")

        # Metrics Breakdown
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Word Count", ats_results["metrics"]["word_count"])
        c2.metric("Action Verbs Used", ats_results["metrics"]["action_verb_count"])
        c3.metric("Quantified Metrics", ats_results["metrics"]["quantifiable_metrics_count"])
        c4.metric("Extracted Skills", skills["count"])

        # Detailed Sections & Skills
        col_skills, col_recs = st.columns([1.2, 0.8])

        with col_skills:
            st.markdown("### 🛠️ Extracted Skills by Category")
            if skills["categorized"]:
                for cat, cat_skills in skills["categorized"].items():
                    with st.expander(f"**{cat}** ({len(cat_skills)})", expanded=True):
                        tags_html = "".join([f'<span class="skill-tag">{s}</span>' for s in cat_skills])
                        st.markdown(tags_html, unsafe_allow_html=True)
            else:
                st.info("No standardized technical skills identified.")

        with col_recs:
            st.markdown("### 💡 ATS Recommendations")
            if ats_results["recommendations"]:
                for rec in ats_results["recommendations"]:
                    st.warning(rec)
            else:
                st.success("🌟 Outstanding resume structure! All core ATS criteria met.")

            st.markdown("### 📑 Section Checklist")
            sec_df = pd.DataFrame([
                {"Section": k, "Status": "✅ Present" if v else "❌ Missing"}
                for k, v in ats_results["sections"].items()
            ])
            st.dataframe(sec_df, hide_index=True, use_container_width=True)

        # Optional AI Feedback
        if gemini_key:
            st.markdown("---")
            st.markdown("### 🤖 Gemini Executive Review & Bullet Rewrites")
            with st.spinner("Generating AI Review..."):
                feedback = get_ai_feedback(resume_input, api_key=gemini_key)
                st.markdown(feedback)
    else:
        st.info("👆 Upload a resume or click 'Load Sample Resume' in the sidebar to get started.")

# --- TAB 2: Job Description Matcher ---
with tab2:
    st.markdown("### 🎯 Match Resume Against a Specific Job Description")
    col_r, col_j = st.columns(2)

    with col_r:
        match_res = st.text_area("Resume Content:", value=SAMPLE_RESUME if load_sample else "", height=220, key="match_r")
    with col_j:
        match_jd = st.text_area("Job Description:", value=SAMPLE_JD if load_sample else "", height=220, key="match_j")

    if st.button("🚀 Analyze Job Match & Skills Gap", type="primary"):
        if match_res.strip() and match_jd.strip():
            match_res_data = match_resume_with_job(match_res, match_jd)

            c_score1, c_score2 = st.columns([1, 2])
            with c_score1:
                st.metric("Overall Match Score", f"{match_res_data['match_score']}%")
                st.metric("TF-IDF Semantic Similarity", f"{match_res_data['cosine_score']}%")

            with c_score2:
                st.write("**Matching Progress**")
                st.progress(int(match_res_data['match_score']))
                if match_res_data['match_score'] >= 75:
                    st.success("🔥 High Match! This candidate is an excellent fit for this position.")
                elif match_res_data['match_score'] >= 50:
                    st.info("👍 Moderate Match. Has core skills but lacks a few specific requirements.")
                else:
                    st.warning("⚠️ Low Match. Consider tailoring the resume with key missing technologies.")

            st.markdown("---")
            col_match_skills, col_miss_skills = st.columns(2)

            with col_match_skills:
                st.markdown(f"#### ✅ Matched Skills ({len(match_res_data['matching_skills'])})")
                if match_res_data['matching_skills']:
                    tags_html = "".join([f'<span class="skill-tag">{s}</span>' for s in match_res_data['matching_skills']])
                    st.markdown(tags_html, unsafe_allow_html=True)
                else:
                    st.write("No direct matching skills found.")

            with col_miss_skills:
                st.markdown(f"#### ❌ Missing Skills ({len(match_res_data['missing_skills'])})")
                if match_res_data['missing_skills']:
                    tags_html = "".join([f'<span class="missing-tag">{s}</span>' for s in match_res_data['missing_skills']])
                    st.markdown(tags_html, unsafe_allow_html=True)
                else:
                    st.write("No critical skills missing!")
        else:
            st.error("Please provide both Resume and Job Description text.")

# --- TAB 3: Batch Resume Ranker ---
with tab3:
    st.markdown("### 📂 Batch Candidate Screening & Ranking")
    st.write("Upload multiple resumes to rank candidates against a single target job description.")

    batch_jd = st.text_area("Target Job Description for Screening:", value=SAMPLE_JD if load_sample else "", height=150)
    uploaded_resumes = st.file_uploader("Upload Multiple Resumes", type=["pdf", "docx", "txt"], accept_multiple_files=True)

    if st.button("⚡ Rank All Resumes", type="primary"):
        if batch_jd.strip() and uploaded_resumes:
            results = []
            for file in uploaded_resumes:
                r_text = extract_text(file)
                contact = extract_contact_info(r_text)
                match_data = match_resume_with_job(r_text, batch_jd)
                ats = calculate_ats_score(r_text)

                results.append({
                    "Filename": file.name,
                    "Candidate Name": contact["name"],
                    "Match Score (%)": match_data["match_score"],
                    "ATS Score (%)": ats["total_score"],
                    "Matched Skills": ", ".join(match_data["matching_skills"][:6]),
                    "Missing Skills Count": len(match_data["missing_skills"])
                })

            df_results = pd.DataFrame(results).sort_values(by="Match Score (%)", ascending=False)

            st.markdown("### 🏆 Candidate Leaderboard")
            st.dataframe(df_results, use_container_width=True)

            # Interactive Bar Chart
            fig_bar = px.bar(
                df_results,
                x="Candidate Name",
                y="Match Score (%)",
                color="Match Score (%)",
                color_continuous_scale="Viridis",
                title="Candidate Match Comparison"
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.error("Please provide a Job Description and at least one Resume file.")

# --- TAB 4: ML Domain Classifier ---
with tab4:
    st.markdown("### 🧠 Machine Learning Domain & Role Predictor")
    st.write("Predicts the professional specialization of a candidate based on NLP text classification.")

    ml_input = st.text_area("Paste Resume or Experience Text for Classification:", value=SAMPLE_RESUME if load_sample else "", height=180)

    if st.button("🔍 Predict Domain with ML"):
        if ml_input.strip():
            prediction = classifier.predict(ml_input)

            st.success(f"🎯 **Predicted Primary Domain:** {prediction['primary_domain']}")

            prob_df = pd.DataFrame(
                list(prediction["probabilities"].items()),
                columns=["Specialization", "Confidence (%)"]
            )

            # Radar / Bar Visualization
            fig_radar = px.bar(
                prob_df,
                x="Confidence (%)",
                y="Specialization",
                orientation='h',
                color="Confidence (%)",
                color_continuous_scale="Blues",
                title="Domain Confidence Distribution"
            )
            st.plotly_chart(fig_radar, use_container_width=True)
        else:
            st.error("Please enter resume text.")
