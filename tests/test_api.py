import io
from unittest.mock import patch
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

MOCK_RESULT = {
    "score": 85.0,
    "matched_skills": ["Python", "Docker"],
    "missing_skills": ["Java"],
    "bonus_skills": ["Kubernetes"],
    "hiring_decision": "strong_match",
    "recommendations": "Candidat potrivit.",
    "interview_questions": ["Q1?", "Q2?", "Q3?"],
    "red_flags": [],
}


def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analyze_returns_valid_json():
    with patch("api.main.process_candidate_match", return_value=MOCK_RESULT):
        pdf_bytes = io.BytesIO(b"%PDF-1.4 fake content")
        response = client.post(
            "/analyze",
            files={"cv_file": ("cv.pdf", pdf_bytes, "application/pdf")},
            data={"job_description": "Python developer cu 3 ani experienta"},
        )
    assert response.status_code == 200
    body = response.json()
    assert "score" in body
    assert "hiring_decision" in body
    assert isinstance(body["interview_questions"], list)


def test_analyze_rejects_invalid_extension():
    txt_bytes = io.BytesIO(b"not a pdf")
    response = client.post(
        "/analyze",
        files={"cv_file": ("cv.txt", txt_bytes, "text/plain")},
        data={"job_description": "Some job"},
    )
    assert response.status_code == 400


def test_analyze_returns_422_on_pipeline_error():
    with patch("api.main.process_candidate_match", return_value={"error": "Pipeline failed"}):
        pdf_bytes = io.BytesIO(b"%PDF fake")
        response = client.post(
            "/analyze",
            files={"cv_file": ("cv.pdf", pdf_bytes, "application/pdf")},
            data={"job_description": "Some job"},
        )
    assert response.status_code == 422
