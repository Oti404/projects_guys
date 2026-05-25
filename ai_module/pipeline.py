import json
from parser import parse_cv
from ner import extract_entities
from embeddings import generate_embeddings
from agent import get_ai_agent_evaluation

def process_candidate_match(cv_file_path: str, jd_text: str) -> dict:
    """
    Acts as the main pipeline for Phase 1 and Phase 2.
    Reads the CV, processes both the CV and Job Description (JD),
    generates skill embeddings, computes math scores, and runs the AI Agent.
    """
    
    # Parse the CV file (PDF or DOCX) to get raw text
    cv_text = parse_cv(cv_file_path)
    if cv_text.startswith("Error"):
        return {"error": cv_text}

    # Extract entities (skills, education, experience) from both CV and JD
    cv_entities = extract_entities(cv_text)
    jd_entities = extract_entities(jd_text)

    cv_skills = cv_entities.get("skills", [])
    jd_skills = jd_entities.get("skills", [])

    cv_skills_text = " ".join(cv_skills)
    jd_skills_text = " ".join(jd_skills)

    cv_vector = generate_embeddings([cv_skills_text])[0].tolist() if cv_skills else []
    jd_vector = generate_embeddings([jd_skills_text])[0].tolist() if jd_skills else []

    final_output = {
        "cv": {
            "skills": cv_skills,
            "skills_vector": cv_vector,
            "years_of_experience": cv_entities.get("years_of_experience"),
            "education": cv_entities.get("education")
        },
        "jd": {
            "skills_required": jd_skills,
            "skills_vector": jd_vector,
            "minimum_experience": jd_entities.get("years_of_experience"), 
            "education_required": jd_entities.get("education")
        }
    }

    # AI Agent evaluation based on the extracted data and computed similarity
    result_matching = get_ai_agent_evaluation(final_output)
    
    return result_matching


if __name__ == "__main__":
    # Fake JD text for testing
    sample_jd = """
    We are looking for a Software Engineer with 3 years of experience.
    Must know Java, FastAPI, and Docker. 
    A degree from a University is required.
    """
    
    # Since you are running this file directly, use the relative path from project root
    result = process_candidate_match("data/raw/sample_cv.pdf", sample_jd)
    print(json.dumps(result, indent=2))