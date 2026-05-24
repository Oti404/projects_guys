import spacy
import re

# Load the English NLP model for spaCy


try:
    nlp = spacy.load("en_core_web_sm", disable=["parser", "lemmatizer"])
except OSError:
    print("The spaCy model was not found. Make sure to run:")
    print("python -m spacy download en_core_web_sm")
    nlp = None

# Expanded list of skills covering the Top 20 frequent words + specific technical/domain skills
KNOWN_SKILLS = [
    "sales", "customer service", "business development", "project management", 
    "training", "marketing", "financial analysis", "data analysis",
    "python", "fastapi", "docker", "java", "c++", "machine learning", 
    "sql", "aws", "react", "javascript", "kubernetes", "rest api", "agile",
    "recruiting", "fmla", "hris", "payroll", "employee relations", "onboarding",
    "gaap", "accounts payable", "accounts receivable", "tax preparation", "auditing",
    "catering", "food safety", "haccp", "patient care", "medical terminology"
]

# The exact 24 unique job categories from the Kaggle dataset
COMMON_TITLES = [
    "information technology", "business development", "advocate", "chef", 
    "finance", "engineering", "accountant", "fitness", "aviation", "sales", 
    "healthcare", "consultant", "banking", "construction", "public relations", 
    "hr", "designer", "arts", "teacher", "apparel", "digital media", 
    "agriculture", "automobile", "bpo", "human resources"
]

def extract_entities(text: str) -> dict:
    """
    Processes the raw text of a CV and returns a structured dictionary 
    with the extracted entities (Name, Title, Experience, Skills, Education, Location).
    """
    if not nlp:
        return {"error": "SpaCy is not initialized."}

    doc = nlp(text)
    text_lower = text.lower()

    # Extract Name 
    name = None
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text
            break

    # Extract Location 
    location = None
    for ent in doc.ents:
        if ent.label_ == "GPE":
            location = ent.text
            break

    # Extract Education
    education_list = []
    edu_keywords = ["university", "college", "universitatea", "institute", "polytechnic", "school"]
    for ent in doc.ents:
        if ent.label_ == "ORG" and any(kw in ent.text.lower() for kw in edu_keywords):
            education_list.append(ent.text)
            
    education = ", ".join(education_list) if education_list else None

    # Extract Skills 
    skills = set()
    for skill in KNOWN_SKILLS:
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            skills.add(skill.title())

    # Extract Years of Experience 
    years_of_experience = None
    exp_pattern = r'(\d+)\+?\s*(years|ani)\s*(of)?\s*(experience|experienta|experiență)'
    match = re.search(exp_pattern, text_lower)
    if match:
        years_of_experience = int(match.group(1))

    # Extract Title 
    title = None
    intro_text = text_lower[:500]
    for job in COMMON_TITLES:
        if job in intro_text:
            title = job.title()
            break

    return {
        "name": name,
        "title": title,
        "years_of_experience": years_of_experience,
        "skills": list(skills),
        "education": education,
        "location": location
    }