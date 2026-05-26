from ai_module.matcher import calculate_skills_similarity, calculate_final_score


def test_similarity_identical_vectors():
    vec = [0.1, 0.2, 0.3]
    score = calculate_skills_similarity(vec, vec)
    assert abs(score - 1.0) < 1e-6


def test_similarity_empty_vectors_returns_zero():
    assert calculate_skills_similarity([], [1.0, 0.0]) == 0.0
    assert calculate_skills_similarity([1.0, 0.0], []) == 0.0
    assert calculate_skills_similarity([], []) == 0.0


def test_similarity_orthogonal_vectors():
    score = calculate_skills_similarity([1.0, 0.0], [0.0, 1.0])
    assert abs(score) < 1e-6


def test_final_score_in_range():
    vec = [0.5, 0.5]
    cv_data = {"skills": ["Python", "Docker"], "skills_vector": vec, "years_of_experience": 3, "education": "university"}
    jd_data = {"skills_required": ["Python", "Java"], "skills_vector": vec, "minimum_experience": 2, "education_required": "university"}
    result = calculate_final_score(1.0, cv_data, jd_data)
    assert 0 <= result["score"] <= 100


def test_final_score_matched_and_missing_skills():
    vec = [0.5, 0.5]
    cv_data = {"skills": ["Python", "Docker"], "skills_vector": vec, "years_of_experience": None, "education": None}
    jd_data = {"skills_required": ["Python", "Java"], "skills_vector": vec, "minimum_experience": None, "education_required": None}
    result = calculate_final_score(1.0, cv_data, jd_data)
    assert "Python" in result["matched_skills"]
    assert "Java" in result["missing_skills"]
    assert "Docker" in result["bonus_skills"]


def test_final_score_empty_skills():
    cv_data = {"skills": [], "skills_vector": [], "years_of_experience": None, "education": None}
    jd_data = {"skills_required": [], "skills_vector": [], "minimum_experience": None, "education_required": None}
    result = calculate_final_score(0.0, cv_data, jd_data)
    assert result["score"] == 0.0
    assert result["matched_skills"] == []
    assert result["missing_skills"] == []
