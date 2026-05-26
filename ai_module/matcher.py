import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def calculate_skills_similarity(cv_vector, jd_vector):
    """Calculates the cosine similarity between the CV and JD embeddings."""
    if not cv_vector or not jd_vector:
        return 0.0

    # Reshape vectors to 2D arrays
    vec_cv = np.array(cv_vector).reshape(1, -1)
    vec_jd = np.array(jd_vector).reshape(1, -1)

    # Calculate cosine similarity 
    similarity = cosine_similarity(vec_cv, vec_jd)[0][0]
    return float(max(0.0, similarity))


def calculate_final_score(
    skills_sim,
    cv_data,
    jd_data,
    weights={"skills": 0.5, "experience": 0.3, "education": 0.2},
):
    """Computes the final weighted percentage match score and handles nulls."""

    # 1. Experience Check
    cv_exp = cv_data.get("years_of_experience")
    jd_exp = jd_data.get("minimum_experience")

    if cv_exp is not None and jd_exp is not None and jd_exp > 0:
        # If candidate has more or equal experience, give 100% for this category
        exp_score = min(1.0, cv_exp / jd_exp)
    else:
        exp_score = skills_sim

    # 2. Education Check
    cv_edu = cv_data.get("education")
    jd_edu = jd_data.get("education_required")

    if cv_edu and jd_edu:
        edu_score = 1.0 if str(jd_edu).lower() in str(cv_edu).lower() else 0.5
    else:
        edu_score = skills_sim 

    # 3. Apply Custom Weights Formula
    final_score = (
        (skills_sim * weights["skills"])
        + (exp_score * weights["experience"])
        + (edu_score * weights["education"])
    )

    # 4. Identify exact matches and gaps
    cv_skills = set([s.lower() for s in cv_data.get("skills", [])])
    jd_skills = set([s.lower() for s in jd_data.get("skills_required", [])])

    matched_skills = list(cv_skills.intersection(jd_skills))
    missing_skills = list(jd_skills.difference(cv_skills))
    bonus_skills = list(cv_skills.difference(jd_skills))

    return {
        "score": round(final_score * 100, 1),
        "matched_skills": [s.capitalize() for s in matched_skills],
        "missing_skills": [s.capitalize() for s in missing_skills],
        "bonus_skills": [s.capitalize() for s in bonus_skills],
    }
