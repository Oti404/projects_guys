"# ai_project_2026"
"# projects_guys"

## 1. Definirea Problemei și Soluția Propusă

### Problema Curentă

În procesele moderne de recrutare, departamentele de HR sunt adesea copleșite de volumul uriaș de CV-uri primite pentru fiecare post. Această evaluare manuală aduce trei provocări majore:

- **Este lentă:** Generează cicluri de angajare prelungite și blochează resursele umane.
- **Este subiectivă:** Procesul este predispus la prejudecăți inconștiente.
- **Este inconsistentă:** Volumul mare duce la omiterea candidaților calificați și oboseală decizională.

### Soluția Noastră: AI HR Assistant

Dezvoltăm un instrument de triere a CV-urilor bazat pe AI care standardizează evaluarea candidaților. **Scopul nu este automatizarea deciziei de angajare**, ci oferirea unui suport decizional rapid și explicabil.

### Fluxul de Date (Input/Output)

- **Input:** CV-ul candidatului (PDF/DOCX) + Descrierea postului (Job Description - text).
- **Procesare:** Sistemul extrage entitățile, calculează similaritatea și analizează potrivirea prin intermediul unui agent Azure OpenAI.
- **Output:**
  1. Scor procentual de potrivire.
  2. Justificare (competențe găsite vs. competențe lipsă).
  3. Recomandări pentru interviu (întrebări personalizate).

### Schema Soluției

<img src="docs/schema.jpg" alt="Schema Arhitecturii" width="600">

[Vezi aici slide-ul pentru prezentarea problemei](docs/Slide_prezentare.pdf)

## Etapa 1: Date & NLP (Setup & Rulare)

Acest modul se ocupă de parsarea CV-urilor, extragerea entităților (NER) și generarea de embeddings.

### Cerințe Importante

Pentru a evita crash-urile de memorie la nivelul sistemului de operare (Segmentation Fault) cauzate de bibliotecile AI (`spaCy`, `sentence-transformers`), **este obligatoriu să folosiți Python 3.12** (versiunile beta ca 3.14 sau mai vechi pot avea probleme cu fișierele precompilate C++ pe Windows).

### 1. Instalare Biblioteci

Asigurați-vă că instalați pachetele specific pentru Python 3.12:
`py -3.12 -m pip install PyPDF2 python-docx spacy sentence-transformers numpy`

### 2. Descărcare Model de Limbă (spaCy)

Descărcați dicționarul pentru limba engleză:
`py -3.12 -m spacy download en_core_web_sm`

### 3. Testare

Pentru a rula un test cap-coadă pe un CV de exemplu:
`py -3.12 example_run.py`
_(Se va descărca automat modelul all-MiniLM-L6-v2 la prima rulare)._

---

## Etapa 2: Agentul AI de Decizie (Setup & Rulare)

Acest modul extinde metricile cantitative calculate în Etapa 1, introducând un strat de analiză calitativă profundă, bazat pe **Azure OpenAI (gpt-4o-mini)**. Modulul folosește caracteristica nativă de **Structured Outputs (JSON Schema)** pentru a garanta că răspunsurile generate de LLM respectă un contract de date strict, eliminând riscul de erori (parsing crashes) la integrarea cu interfața grafică.

### 1. Instalare Dependențe Suplimentare

Pentru această etapă, pe lângă librăriile de NLP din prima fază, este necesară instalarea SDK-ului oficial OpenAI și a utilitarului pentru procesarea variabilelor de mediu:

```bash
.venv\Scripts\python.exe -m pip install python-dotenv openai
```

### 2. Rularea și Verificarea Pipeline-ului

Orchestratorul principal îmbină acum cele două etape: extragerea datelor matematice (vectori de similaritate, skill-uri lipsă/bonus) și trimiterea lor către Agentul AI pentru raportul calitativ. 

Pentru a rula o verificare cap-la-cap direct din terminal, asigură-te că te afli în folderul rădăcină al proiectului și rulează:

```powershell
# Setează calea proiectului pentru ca Python să poată rezolva importurile absolute interne
$env:PYTHONPATH="."

# Rulează scriptul orchestrator
.venv\Scripts\python.exe -m ai_module.pipeline
```

### 3. Contractul de Date pentru Etapa 3 (UI / Frontend)

Funcția `process_candidate_match` din interiorul `ai_module/pipeline.py` reprezintă punctul unic de intrare pentru interfața grafică. Ea returnează un dicționar Python (payload JSON) cu o structură strictă și predictibilă:

```json
{
  "score": 62.7,
  "matched_skills": ["Fastapi", "Docker"],
  "missing_skills": ["Java"],
  "bonus_skills": ["Python", "Sql", "Javascript"],
  "hiring_decision": "partial_match",
  "recommendations": "The candidate is not suitable for the position due to a complete lack of required experience...",
  "interview_questions": [
    "Can you explain any projects or experiences where you utilized FastAPI or Docker?",
    "What is your understanding of Java and how do you plan to acquire this skill?",
    "Can you discuss how your bonus skills in Python, SQL, or JavaScript could contribute to this role?"
  ],
  "red_flags": [
    "Candidate has no professional experience, which is significantly below the required 3 years.",
    "Candidate has no formal education, which does not meet the university degree requirement."
  ]
}
```

#### Criterii de Validare Automată:
- **`hiring_decision`**: Este calculat în mod determinist pe baza scorului final și poate lua doar următoarele valori string fixe: `"strong_match"` (>= 85), `"good_match"` (>= 70), `"partial_match"` (>= 50), `"weak_match"` (< 50) sau `"evaluation_error"`.
- **`interview_questions`**: Schema blochează LLM-ul să returneze mai mult sau mai puțin de **exact 3 întrebări** personalizate pe baza lipsurilor sau a skill-urilor bonus detectate.