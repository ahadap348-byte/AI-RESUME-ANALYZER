"""
NLP Information Extraction and Text Processing.
"""
import re
from typing import Dict, List, Any
from utils.skills_db import SKILLS_DB

# Regular expressions for contact info
EMAIL_REGEX = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
PHONE_REGEX = r'(\+?\d{1,3}[-.\s]?)?(\(?\d{2,4}\)?[-.\s]?)?\d{3,4}[-.\s]?\d{3,4}'
LINKEDIN_REGEX = r'(https?:\/\/)?(www\.)?linkedin\.com\/in\/[a-zA-Z0-9_-]+'
GITHUB_REGEX = r'(https?:\/\/)?(www\.)?github\.com\/[a-zA-Z0-9_-]+'

ACTION_VERBS = [
    "accelerated", "achieved", "analyzed", "architected", "automated", "built",
    "collaborated", "created", "decreased", "delivered", "deployed", "designed",
    "developed", "engineered", "enhanced", "established", "executed", "expanded",
    "generated", "implemented", "improved", "increased", "initiated", "integrated",
    "launched", "led", "managed", "maximized", "migrated", "minimized", "modeled",
    "optimized", "orchestrated", "overhauled", "pioneered", "reduced", "refactored",
    "resolved", "scaled", "spearheaded", "standardized", "streamlined", "transformed"
]

COMMON_DEGREES = [
    "bachelor", "bachelors", "b.s.", "bs", "b.tech", "btech", "b.e.", "be", "bba", "bca",
    "master", "masters", "m.s.", "ms", "m.tech", "mtech", "m.e.", "mba", "mca",
    "ph.d", "phd", "doctorate", "associate", "diploma"
]

SECTION_KEYWORDS = {
    "Summary": ["summary", "objective", "profile", "about me", "professional summary"],
    "Experience": ["experience", "employment", "work history", "work experience", "career"],
    "Education": ["education", "academic", "qualifications", "degrees", "university", "college"],
    "Skills": ["skills", "technical skills", "technologies", "competencies", "tools"],
    "Projects": ["projects", "personal projects", "portfolio", "key projects"],
    "Certifications": ["certifications", "certificates", "licenses", "courses", "credentials"]
}


def clean_text(text: str) -> str:
    """Normalize text by lowering and removing irregular characters."""
    text = re.sub(r'[\r\n\t]+', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9\s.,@/+#-]', ' ', text)
    return ' '.join(text.split())


def extract_contact_info(text: str) -> Dict[str, Any]:
    """Extract email, phone, links, and estimate name."""
    emails = re.findall(EMAIL_REGEX, text)
    linkedin = re.findall(LINKEDIN_REGEX, text)
    github = re.findall(GITHUB_REGEX, text)

    # Clean phone numbers
    valid_phones = []
    for match in re.finditer(PHONE_REGEX, text):
        phone_str = match.group(0).strip()
        digits = re.sub(r'\D', '', phone_str)
        if 9 <= len(digits) <= 15:
            valid_phones.append(phone_str)

    # Candidate Name estimation (first non-empty line, if it looks like a name)
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    estimated_name = "Candidate"
    if lines:
        first_line = lines[0]
        if "@" not in first_line and not re.search(r'\d', first_line) and len(first_line.split()) <= 4:
            estimated_name = first_line

    return {
        "name": estimated_name,
        "email": emails[0] if emails else "Not Found",
        "phone": valid_phones[0] if valid_phones else "Not Found",
        "linkedin": "LinkedIn Found" if "linkedin.com" in text.lower() else "Not Found",
        "github": "GitHub Found" if "github.com" in text.lower() else "Not Found"
    }


def extract_skills(text: str) -> Dict[str, List[str]]:
    """Identify skills from the resume and group by category."""
    text_lower = f" {text.lower()} "
    found_categorized = {}
    total_found = set()

    for category, skills in SKILLS_DB.items():
        matched = []
        for skill in skills:
            # Match whole words / phrases
            pattern = r'(?<![a-zA-Z0-9])' + re.escape(skill) + r'(?![a-zA-Z0-9])'
            if re.search(pattern, text_lower):
                matched.append(skill.title())
                total_found.add(skill)
        if matched:
            found_categorized[category] = matched

    return {
        "categorized": found_categorized,
        "all_skills": sorted(list(total_found)),
        "count": len(total_found)
    }


def detect_sections(text: str) -> Dict[str, bool]:
    """Check whether core standard resume sections are present."""
    text_lower = text.lower()
    results = {}
    for section, keywords in SECTION_KEYWORDS.items():
        found = any(re.search(r'\b' + re.escape(kw) + r'\b', text_lower) for kw in keywords)
        results[section] = found
    return results


def analyze_quality_metrics(text: str) -> Dict[str, Any]:
    """Calculate quantifiable metrics: action verbs, metrics/numbers, word count."""
    words = text.lower().split()
    word_count = len(words)

    # Action verbs count
    verbs_used = [verb for verb in ACTION_VERBS if re.search(r'\b' + verb + r'\b', text.lower())]

    # Quantifiable metrics (e.g., 20%, $50K, 10x, 150 users)
    metrics_patterns = re.findall(r'(\d+[\.,]?\d*[%kKmMxX+]|\$\d+[\.,]?\d*|\b\d+\b)', text)

    return {
        "word_count": word_count,
        "action_verbs": list(set(verbs_used)),
        "action_verb_count": len(set(verbs_used)),
        "quantifiable_metrics_count": len(metrics_patterns)
    }
