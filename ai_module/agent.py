import os
import json
from dotenv import load_dotenv
from openai import AzureOpenAI

from matcher import (
    calculate_skills_similarity,
    calculate_final_score
)

# Load environment variables
load_dotenv()

# Azure OpenAI client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-08-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)
SYSTEM_PROMPT = """
You are a Senior Technical Recruiter and Talent Assessment Specialist.

Your responsibility is to evaluate candidate-job fit using ONLY the structured data provided by the system.

EVALUATION RULES

1. Be objective, professional, and evidence-based.
2. Never invent skills, experience, certifications, projects, education, or achievements.
3. Use only the information explicitly provided.
4. Missing required skills should be treated as meaningful gaps.
5. Distinguish clearly between:
   - matched skills
   - missing skills
   - bonus skills
   - experience alignment
   - education alignment
6. If experience is below requirements, explicitly mention it.
7. If education does not satisfy requirements, explicitly mention it.
8. Recommendations must explain WHY the candidate is or is not a suitable fit.
9. Interview questions must focus on:
   - validating missing skills
   - validating claimed experience
   - exploring bonus skills that could add value
10. Red flags must represent actual hiring risks supported by the data.
11. Avoid generic statements and vague HR language.
12. Do not assume the candidate possesses skills that are not listed.

RECOMMENDATION STYLE

- Be concise but informative.
- Focus on evidence.
- Explain strengths and weaknesses.
- Mention important skill gaps.
- Mention experience mismatches when relevant.
"""

JSON_SCHEMA = {
    "name": "candidate_evaluation",
    "schema": {
        "type": "object",
        "properties": {
            "recommendations": {
                "type": "string"
            },
            "interview_questions": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "minItems": 3,
                "maxItems": 3
            },
            "red_flags": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            }
        },
        "required": [
            "recommendations",
            "interview_questions",
            "red_flags"
        ],
        "additionalProperties": False
    }
}


def get_ai_agent_evaluation(stage1_output: dict) -> dict:
    """
    Stage 2 AI evaluation.

    Receives parsed CV/JD data and matching metrics,
    then generates recruiter-oriented qualitative analysis.
    """

    cv_data = stage1_output.get("cv", {})
    jd_data = stage1_output.get("jd", {})

    # Mathematical matching engine
    similarity = calculate_skills_similarity(
        cv_data.get("skills_vector"),
        jd_data.get("skills_vector")
    )

    match_analysis = calculate_final_score(
        similarity,
        cv_data,
        jd_data
    )

    user_content = f"""
    Candidate Evaluation Data

    MATCH SCORE:
    {match_analysis['score']}%

    MATCHED SKILLS:
    {match_analysis['matched_skills']}

    MISSING SKILLS:
    {match_analysis['missing_skills']}

    BONUS SKILLS:
    {match_analysis['bonus_skills']}

    CANDIDATE PROFILE

    Years of Experience:
    {cv_data.get('years_of_experience')}

    Education:
    {cv_data.get('education')}

    JOB REQUIREMENTS

    Minimum Experience:
    {jd_data.get('minimum_experience')}

    Required Education:
    {jd_data.get('education_required')}

    Generate:

    1. A recruiter recommendation.
    2. Three targeted interview questions.
    3. Two meaningful red flags.

    Base your analysis strictly on the provided information.
    """

    try:
        response = client.chat.completions.create(
            model=os.getenv(
                "AZURE_OPENAI_DEPLOYMENT_NAME",
                "gpt-4o-mini"
            ),
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_content
                }
            ],
            response_format={
                "type": "json_schema",
                "json_schema": JSON_SCHEMA
            },
            temperature=0.2
        )

        parsed = json.loads(response.choices[0].message.content)

        score = match_analysis["score"]

        if score >= 85:
            hiring_decision = "strong_match"
        elif score >= 70:
            hiring_decision = "good_match"
        elif score >= 50:
            hiring_decision = "partial_match"
        else:
            hiring_decision = "weak_match"

        return {
            "score": match_analysis["score"],
            "matched_skills": match_analysis["matched_skills"],
            "missing_skills": match_analysis["missing_skills"],
            "bonus_skills": match_analysis["bonus_skills"],

            "hiring_decision": hiring_decision,

            "recommendations": parsed.get("recommendations", ""),
            "interview_questions": parsed.get("interview_questions", []),
            "red_flags": parsed.get("red_flags", [])
        }
    
    except Exception as e:
        return {
            "error": f"Agent AI Integration failed: {str(e)}",
            "score": match_analysis["score"],
            "weights_applied": match_analysis.get("weights_applied"),
            "matched_skills": match_analysis["matched_skills"],
            "missing_skills": match_analysis["missing_skills"],
            "bonus_skills": match_analysis["bonus_skills"],
            "hiring_decision": "evaluation_error",
            "recommendations": "AI evaluation unavailable. Review quantitative matching results.",
            "interview_questions": [],
            "red_flags": ["Azure OpenAI evaluation unavailable"]
        }