"""
Scoring Engine: ATS Quality Score & Job Description Matcher.
"""
from typing import Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.nlp_parser import detect_sections, analyze_quality_metrics, extract_skills, clean_text


def calculate_ats_score(resume_text: str) -> Dict[str, Any]:
    """
    Calculate an ATS score out of 100 based on:
    - Section Completeness (30 pts)
    - Action Verbs (20 pts)
    - Quantifiable Metrics & Results (20 pts)
    - Skill Variety (20 pts)
    - Length / Formatting (10 pts)
    """
    sections = detect_sections(resume_text)
    metrics = analyze_quality_metrics(resume_text)
    skills = extract_skills(resume_text)

    # 1. Section Completeness (up to 30)
    section_score = sum(6 for s, present in sections.items() if present)

    # 2. Action Verbs (up to 20)
    verb_count = metrics["action_verb_count"]
    verb_score = min(20, verb_count * 2)

    # 3. Quantifiable Metrics (up to 20)
    quant_count = metrics["quantifiable_metrics_count"]
    quant_score = min(20, quant_count * 2)

    # 4. Skills count (up to 20)
    skill_count = skills["count"]
    skill_score = min(20, skill_count * 2)

    # 5. Length score (up to 10)
    word_count = metrics["word_count"]
    if 300 <= word_count <= 900:
        length_score = 10
    elif 200 <= word_count < 300 or 900 < word_count <= 1400:
        length_score = 7
    else:
        length_score = 4

    total_score = min(100, section_score + verb_score + quant_score + skill_score + length_score)

    # Improvement recommendations
    recommendations = []
    for sec, present in sections.items():
        if not present:
            recommendations.append(f"Add a clear **{sec}** section to improve ATS parsability.")
    if verb_count < 6:
        recommendations.append("Use more strong **action verbs** (e.g., *Spearheaded, Architected, Automated, Reduced*).")
    if quant_count < 4:
        recommendations.append("Include more **quantified results** (e.g., *'Improved latency by 35%'*, *'Handled 100k+ daily users'*).")
    if skill_count < 8:
        recommendations.append("List more specific industry tools and technical skills.")

    return {
        "total_score": total_score,
        "breakdown": {
            "Sections": f"{section_score}/30",
            "Action Verbs": f"{verb_score}/20",
            "Quantified Impact": f"{quant_score}/20",
            "Skills Diversity": f"{skill_score}/20",
            "Length & Flow": f"{length_score}/10"
        },
        "sections": sections,
        "metrics": metrics,
        "recommendations": recommendations
    }


def match_resume_with_job(resume_text: str, jd_text: str) -> Dict[str, Any]:
    """
    Computes matching percentage between a Resume and a Job Description.
    """
    if not resume_text.strip() or not jd_text.strip():
        return {"match_score": 0, "cosine_score": 0, "matching_skills": [], "missing_skills": []}

    # 1. TF-IDF & Cosine Similarity
    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000, ngram_range=(1, 2))
    cleaned_resume = clean_text(resume_text)
    cleaned_jd = clean_text(jd_text)
    tfidf_matrix = vectorizer.fit_transform([cleaned_resume, cleaned_jd])
    sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    cosine_pct = round(float(sim) * 100, 1)

    # 2. Skill Gap Analysis
    resume_skills = set(extract_skills(resume_text)["all_skills"])
    jd_skills = set(extract_skills(jd_text)["all_skills"])
    matching_skills = sorted(list(resume_skills.intersection(jd_skills)))
    missing_skills = sorted(list(jd_skills - resume_skills))

    # Weighted Overall Match (60% Skill overlap + 40% TF-IDF Cosine Similarity)
    if jd_skills:
        skill_match_pct = (len(matching_skills) / len(jd_skills)) * 100
        combined_score = round((0.6 * skill_match_pct) + (0.4 * cosine_pct), 1)
    else:
        combined_score = cosine_pct
    combined_score = min(100.0, max(0.0, combined_score))

    return {
        "match_score": combined_score,
        "cosine_score": cosine_pct,
        "matching_skills": [s.title() for s in matching_skills],
        "missing_skills": [s.title() for s in missing_skills],
        "total_jd_skills_count": len(jd_skills)
    }
