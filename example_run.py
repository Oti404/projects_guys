import json
from ai_module.pipeline import process_candidate_match


sample_jd = """
We are looking for a Software Engineer with 3 years of experience.
Must know Java, FastAPI, and Docker. 
A degree from a University is required.
"""

rezultat = process_candidate_match("data/raw/sample_cv.pdf", sample_jd)

print(json.dumps(rezultat, indent=2))