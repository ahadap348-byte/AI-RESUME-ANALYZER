# 🎯 AI Resume Analyzer & Job Matcher

An interactive Streamlit application that uses NLP and Machine Learning to analyze resumes, score them for ATS (Applicant Tracking System) compatibility, match them against job descriptions, and classify candidates into tech domains.

## 📌 Key Features

- **Multi-Format Text Extraction** — Extracts text from PDF, DOCX, and TXT resumes.
- **Entity & Contact Extraction** — Parses Name, Email, Phone, LinkedIn/GitHub links using Regex & NLP.
- **Deep Skills Extraction & Categorization** — Detects 150+ technical and soft skills across 7 categories (Programming Languages, Web & Frontend, Backend, Data Science & ML, Databases, Cloud & DevOps, Soft Skills).
- **ATS Resume Health Score (0–100%)** — Scored on section completeness, action verb density, quantified achievements, skill variety, and formatting/length.
- **Job Description Matching & Gap Analysis** — TF-IDF & Cosine Similarity scoring plus matched vs. missing skills.
- **ML Role Recommender** — TF-IDF + Multinomial Naive Bayes classifier that categorizes resumes into roles (Data Science & AI, Full Stack & Web Dev, Cloud & DevOps, Mobile Development, Cybersecurity, Product Management).
- **Batch Resume Ranker** — Upload multiple resumes and rank candidates against one job description.
- **Optional AI Deep Suggestions** — Google Gemini API integration for bullet-point rewrites and interview prep questions.
- **Interactive Visualizations** — Plotly gauge charts, bar charts, and leaderboard tables.

## 📂 Project Structure

```
ai-resume-analyzer/
│
├── app.py                      # Main Streamlit Web Application
├── requirements.txt            # Python Dependencies
├── README.md                   # Project Documentation
│
├── utils/
│   ├── __init__.py
│   ├── extractor.py            # PDF / DOCX / TXT Parser
│   ├── nlp_parser.py           # NLP Entities, Contact Info, Action Verbs
│   ├── skills_db.py            # Skills Dictionary/Taxonomy
│   ├── scorer.py               # ATS Scoring & JD Matcher
│   ├── classifier.py           # ML Job Category Classifier
│   └── gemini_advisor.py       # Optional LLM Advice Generator
│
└── samples/
    ├── sample_resume.txt
    └── sample_jd.txt
```

## 🛠️ Installation & Setup

### 1. Clone / extract the project and navigate into it
```bash
cd ai-resume-analyzer
```

### 2. Create a virtual environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
streamlit run app.py
```

The app will launch in your browser at **http://localhost:8501**.

## 💡 How It Works

- **Information Extraction** — Regex-based extraction of emails, phone numbers, LinkedIn/GitHub links, and degree credentials.
- **Skill Taxonomy Matching** — Boundary-sensitive regex pattern matching against a multi-tier skills database to avoid false-positive substring matches.
- **TF-IDF & Cosine Similarity** — Computes vocabulary/semantic alignment between resume and job description text.
- **Weighted ATS Score** — Section presence (30%), action verb density (20%), quantified achievements (20%), skill variety (20%), document length (10%).
- **Multinomial Naive Bayes Classifier** — Classifies resumes into functional tech tracks with a probability distribution.

## 🔑 Optional: Enable Gemini AI Deep Feedback

To unlock AI-generated bullet-point rewrites and interview prep questions, enter a Google Gemini API key in the sidebar of the running app (or set the `GEMINI_API_KEY` environment variable). This feature is fully optional — all core scoring, matching, and classification features work without it.

## 📦 Requirements

See `requirements.txt`. Core libraries: `streamlit`, `pdfplumber`, `pypdf`, `python-docx`, `scikit-learn`, `pandas`, `numpy`, `plotly`.
