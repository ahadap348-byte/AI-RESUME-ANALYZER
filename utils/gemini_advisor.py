"""
Optional AI Advisor using Google Gemini API.
"""
import os

try:
    from google import genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False


def get_ai_feedback(resume_text: str, jd_text: str = "", api_key: str = "") -> str:
    """Generate professional AI review using Gemini."""
    key = api_key or os.environ.get("GEMINI_API_KEY")
    if not key:
        return "⚠️ Please provide a Gemini API Key in the sidebar to enable AI-powered deep feedback."
    if not HAS_GENAI:
        return "⚠️ `google-genai` library is not installed."

    try:
        client = genai.Client(api_key=key)
        prompt = f"""
        You are an expert Executive Tech Recruiter and ATS Specialist.
        Analyze this resume and provide:
        1. Three actionable bullet-point rewrites with quantified impact (XYZ formula: Accomplished [X] as measured by [Y] by doing [Z]).
        2. Top 3 interview questions likely to be asked based on this resume.
        3. Clear recommendations to stand out for the target role.

        RESUME TEXT:
        {resume_text[:3000]}

        TARGET JOB DESCRIPTION (if provided):
        {jd_text[:1500] if jd_text else "General Tech Role"}
        """
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error contacting Gemini API: {str(e)}"
