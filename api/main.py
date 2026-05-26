import os
import tempfile
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from ai_module.pipeline import process_candidate_match
from ai_module.parser import parse_cv
from ai_module.ner import extract_entities

app = FastAPI(title="HR Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


JD_DIR = Path(__file__).parent.parent / "data" / "job_descriptions"


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/job-descriptions")
def list_job_descriptions():
    if not JD_DIR.exists():
        return {"categories": []}
    names = sorted(p.stem for p in JD_DIR.glob("*.txt"))
    return {"categories": names}


@app.get("/job-descriptions/{name}")
def get_job_description(name: str):
    safe_name = Path(name).name  # strip any path traversal
    path = JD_DIR / f"{safe_name}.txt"
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Job description '{name}' negasit.")
    return {"name": safe_name, "content": path.read_text(encoding="utf-8")}


@app.post("/analyze")
async def analyze(
    cv_file: UploadFile = File(...),
    job_description: str = Form(...),
):
    suffix = os.path.splitext(cv_file.filename)[1].lower()
    if suffix not in (".pdf", ".docx"):
        raise HTTPException(status_code=400, detail="Fisierul CV trebuie sa fie PDF sau DOCX.")

    contents = await cv_file.read()

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        result = process_candidate_match(tmp_path, job_description)
    finally:
        os.unlink(tmp_path)

    if "error" in result:
        raise HTTPException(status_code=422, detail=result["error"])

    return result


@app.post("/debug")
async def debug(
    cv_file: UploadFile = File(...),
    job_description: str = Form(...),
):
    """Returnează entitățile extrase din CV și JD fără să apeleze agentul AI."""
    suffix = os.path.splitext(cv_file.filename)[1].lower()
    if suffix not in (".pdf", ".docx"):
        raise HTTPException(status_code=400, detail="Fisierul CV trebuie sa fie PDF sau DOCX.")

    contents = await cv_file.read()

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        cv_text = parse_cv(tmp_path)
    finally:
        os.unlink(tmp_path)

    if cv_text.startswith("Error"):
        raise HTTPException(status_code=422, detail=cv_text)

    cv_entities = extract_entities(cv_text)
    jd_entities = extract_entities(job_description)

    return {
        "cv_extracted": {
            "name": cv_entities.get("name"),
            "title": cv_entities.get("title"),
            "skills": cv_entities.get("skills", []),
            "years_of_experience": cv_entities.get("years_of_experience"),
            "education": cv_entities.get("education"),
            "location": cv_entities.get("location"),
        },
        "jd_extracted": {
            "skills": jd_entities.get("skills", []),
            "years_of_experience": jd_entities.get("years_of_experience"),
            "education_required": jd_entities.get("education"),
        },
        "cv_text_preview": cv_text[:500],
    }
