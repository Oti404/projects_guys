import spacy
import re
from datetime import datetime

# Load the English NLP model for spaCy


try:
    nlp = spacy.load("en_core_web_sm", disable=["parser", "lemmatizer"])
except OSError:
    print("The spaCy model was not found. Make sure to run:")
    print("python -m spacy download en_core_web_sm")
    nlp = None

# Expanded list of skills covering the Top 20 frequent words + specific technical/domain skills
KNOWN_SKILLS = [
    # Business & Management
    "sales", "customer service", "business development", "project management",
    "training", "marketing", "financial analysis", "data analysis", "agile",
    "scrum", "leadership", "communication", "problem solving", "teamwork",

    # Software Engineering
    "python", "fastapi", "docker", "java", "c++", "c#", "go", "rust", "php",
    "machine learning", "deep learning", "nlp", "computer vision",
    "sql", "mysql", "postgresql", "mongodb", "redis",
    "aws", "azure", "gcp", "cloud computing",
    "react", "angular", "vue", "javascript", "typescript", "html", "css",
    "kubernetes", "rest api", "graphql", "microservices", "devops", "ci/cd",
    "git", "linux", "bash", "node.js", "spring", "django", "flask",

    # IT & Networking
    "tcp/ip", "active directory", "microsoft office", "cisco", "itsm",
    "network administration", "network security", "firewall", "vpn",
    "troubleshooting", "technical support", "help desk", "it support",
    "windows server", "linux server", "virtualization", "vmware",
    "cybersecurity", "information security", "information assurance",
    "cyber network defense", "penetration testing", "vulnerability assessment",
    "siem", "ids", "ips", "dns", "dhcp", "ldap", "ethernet",
    "hardware", "desktop support", "system administration",
    "it service management", "remedy", "avaya", "itil",

    # HR
    "recruiting", "fmla", "hris", "payroll", "employee relations", "onboarding",

    # Finance
    "gaap", "accounts payable", "accounts receivable", "tax preparation", "auditing",

    # Healthcare
    "patient care", "medical terminology", "hipaa",

    # Other
    "catering", "food safety", "haccp",
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

    # Primary: spaCy ORG entities
    for ent in doc.ents:
        if ent.label_ == "ORG" and any(kw in ent.text.lower() for kw in edu_keywords):
            education_list.append(ent.text)

    # Fallback: regex for degree lines (e.g. "Bachelor of Science, ... University")
    if not education_list:
        degree_pattern = r'(bachelor|master|phd|doctorate|associate|b\.?s\.?|m\.?s\.?|b\.?a\.?|m\.?a\.?)'
        if re.search(degree_pattern, text_lower):
            education_list.append("University degree detected")

    education = ", ".join(education_list) if education_list else None

    # Extract Skills 
    skills = set()
    for skill in KNOWN_SKILLS:
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            skills.add(skill.title())

    # Extract Years of Experience
    # 1. Explicit "X years of experience"
    years_of_experience = None
    exp_pattern = r'(\d+)\+?\s*(years|ani)\s*(of)?\s*(experience|experienta|experiență)'
    match = re.search(exp_pattern, text_lower)
    if match:
        years_of_experience = int(match.group(1))

    # 2. Fallback: infer from earliest job start year in date ranges
    #    e.g. "Aug 2007 to Current", "2005 to Present"
    if years_of_experience is None:
        months = r'(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|' \
                 r'january|february|march|april|may|june|july|august|' \
                 r'september|october|november|december)'
        date_range_pattern = rf'(?:{months}\s+)?(\d{{4}})\s+to\s+(?:current|present|now)'
        year_matches = re.findall(date_range_pattern, text_lower)
        if year_matches:
            earliest = min(int(y) for y in year_matches)
            current_year = datetime.now().year
            years_of_experience = current_year - earliest

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