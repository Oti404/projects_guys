# CV Parsing & HR Assistant — Plan de Proiect

## Context

- **Echipă:** 3 persoane
- **Săptămâna curentă:** 12 (prezentarea Fazei 1 este ACUM)
- **Obiectiv:** Construim rapid, dar învățăm corect pe parcurs
- **LLM:** Azure OpenAI (avem $200 credit) — alegerea principală
- **Fallback:** Model local prin Ollama dacă Azure se termină

---

## Decizia LLM — Folosim Azure OpenAI

Avem $200 pe Azure — mai mult decât suficient pentru întregul proiect.

- Folosim **Azure OpenAI** cu **GPT-4o mini** (ieftin, rapid, foarte capabil)
- Upgradăm la **GPT-4o** doar pentru raționament complex dacă e nevoie
- $200 la prețurile GPT-4o mini (~$0.15/1M tokeni input) = practic nelimitat pentru un proiect studențesc
- Azure ne dă un endpoint curat, fără bătăi de cap la setup, și contează ca tooling profesional

**Nu folosim Gemini** — free tier-ul are rate limits care ne vor frustra în mijlocul unui demo.

**Modele locale doar ca fallback** — Ollama + Llama 3.1 8B merge pentru NER și matching de bază, dar e slab la raționament complex.

---

## Roluri în Echipă (3 persoane)

Fiindcă suntem 3, două roluri se combină:

| Rol | Persoană | Responsabilități |
|-----|----------|-----------------|
| **Agent AI + Scoring** |    | Integrare LLM/Azure OpenAI, agent cu tool use, prompt engineering, scor de potrivire, explicabilitate |
| **Date & NLP** |     | Colectare date, parsare PDF/DOCX, NER cu spaCy (skills, educație, experiență), embeddings |
| **Integrare & UI** |     | Backend FastAPI, dashboard Streamlit, testare, notebook-uri pentru prezentări |

---

## Arhitectura Soluției

```
Input: CV (PDF/DOCX) + Descriere Post (text)
        ↓
[Persoana Date & NLP]
Parsare             → PyPDF2, python-docx
NLP / NER           → spaCy (extrage: skills, educație, experiență, locație)
Embeddings          → Sentence-BERT (all-MiniLM-L6-v2)
        ↓
[AI Person]
Motor de Potrivire  → Similaritate cosinus + scor ponderat
Agent AI            → Azure OpenAI GPT-4o mini cu tool use
Tooluri agentului:
  - parse_cv()
  - parse_job_description()
  - calculate_match()
  - generate_recommendations()
        ↓
[Persoana Integrare & UI]
API                 → FastAPI POST /analyze
Dashboard           → Streamlit (upload CV, lipești JD, vezi rezultatele)
        ↓
Output: Scor potrivire %, skills lipsă, skills potrivite, întrebări interviu, red flags
```

---

## URGENT — Prezentarea de Mâine Seară (Faza 1, 200 pct)

Trebuie să prezentăm: **definirea problemei + analiza datelor**.
Nu avem nevoie de cod funcțional încă — doar să demonstrăm că înțelegem datele și problema.

### Ce pregătim azi seară:

**1. Slide-ul problemei (5 min, orice format)**
- Echipele HR primesc sute de CV-uri pe post → review manual e lent, subiectiv, inconsistent
- Agentul nostru: automatizează trierea, calculează scorul de potrivire, explică de ce, sugerează întrebări de interviu
- Input: CV + Descriere Post → Output: scor potrivire + recomandări

**2. Notebook rapid de explorare date**
- Descarcă [dataset-ul Kaggle cu CV-uri](https://www.kaggle.com/datasets/gauravduttakiit/resume-dataset) — 2400 CV-uri etichetate pe categorie
- Încarcă în notebook, arată: distribuția categoriilor, număr de cuvinte, cele mai comune skills pe categorie
- 20 de linii de pandas + matplotlib e suficient

**3. Schema soluției**
- Desenează arhitectura de mai sus ca flowchart simplu
- Tools: draw.io, Excalidraw, sau chiar desenat de mână și fotografiat

**4. Demo extragere entități (bonus, impresionant)**
- Rulează spaCy pe 2-3 CV-uri sample și arată ce extrage
- Durează ~30 minute să setezi

---

## Timeline Complet (Revizuit)

### Faza 1 — Problemă + Date (Săpt. 12, 200 pct) ← SUNTEM AICI
- [x] Definit problema și arhitectura
- [ ] Notebook explorare date
- [ ] Schema soluției
- [ ] Prezentare mâine seară

### Faza 2 — Dezvoltare Model (Săpt. 14, 300 pct)
- [ ] Extractor text CV/JD (PDF → text)
- [ ] Pipeline NER cu spaCy (skills, educație, experiență)
- [ ] Embeddings Sentence-BERT + matcher cosinus
- [ ] Formula de scoring ponderată (skills 50%, experiență 30%, educație 20%)
- [ ] Output explicabilitate (skills potrivite vs. lipsă)
- [ ] Agent Azure OpenAI cu tool use
- [ ] Evaluare pe 20-50 perechi CV/JD
- [ ] Notebook-uri: `03_matching_engine.ipynb`, `04_agent_demo.ipynb`

### Faza 3 — Îmbunătățiri (Săpt. 14, 300 pct)
- [ ] Reducerea biasului: eliminăm nume/gen/vârstă/poză înainte de scoring
- [ ] Dashboard Streamlit (upload CV + lipești JD → raport complet)
- [ ] Endpoint FastAPI `POST /analyze`
- [ ] Feedback loop: stocăm thumbs up/down, re-ponderam scorurile în timp
- [ ] Notebook: `05_bias_reduction.ipynb`

### Faza 4 — Video Teaser (Săpt. 14, 200 pct)
- Înregistrare ecran 2-3 min cu fluxul complet
- Menționăm SDG 8 (Muncă Decentă) și SDG 10 (Inegalități Reduse)

---

## Structura Repository-ului

```
projects_guys/
├── README.md                    ← membri echipă, descriere problemă, schema soluției
├── requirements.txt
├── .gitignore
├── data/
│   ├── raw/                     ← git-ignored, se descarcă separat
│   └── processed/               ← git-ignored
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_entity_extraction.ipynb
│   ├── 03_matching_engine.ipynb
│   ├── 04_agent_demo.ipynb
│   └── 05_bias_reduction.ipynb
├── ai_module/
│   ├── parser.py                ← PDF/DOCX → text
│   ├── ner.py                   ← extragere entități spaCy
│   ├── embeddings.py            ← wrapper Sentence-BERT
│   ├── matcher.py               ← scoring + explicabilitate
│   ├── agent.py                 ← agent Azure OpenAI + tooluri
│   └── bias.py                  ← reducere bias
├── api/
│   └── main.py                  ← FastAPI
├── ui/
│   └── app.py                   ← dashboard Streamlit
├── tests/
    ├── test_parser.py
    └── test_matcher.py
```

---

## Stack Tehnologic

| Strat | Tehnologie |
|-------|-----------|
| Limbaj | Python 3.11+ |
| Parsare CV/JD | PyPDF2, python-docx |
| NLP / NER | spaCy (`en_core_web_sm`) |
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`) |
| LLM / Agent | Azure OpenAI (GPT-4o mini) |
| API | FastAPI + Uvicorn |
| UI | Streamlit |
| Testare | pytest |

---

## Surse de Date

- **CV-uri:** Kaggle Resume Dataset — 2400+ CV-uri etichetate pe categorie profesională
- **Descrieri posturi:** LinkedIn Job Postings dataset (Kaggle)
- **Supliment:** Perechi sintetice CV/JD generate prin agent pentru cazuri limită și testare bias

Datele brute sunt git-ignored. Adăugăm un `data/README.md` cu instrucțiuni de descărcare.

---

## Decizii Deschise (discutăm cu echipa)

1. **Cine ia ce rol** — atribuim numele în tabelul de mai sus
2. **Setup Azure** — cine creează resursa Azure OpenAI și împarte cheia prin `.env`
3. **Notebook-uri vs. scripturi pure** — notebook-uri pentru demo/prezentări, module Python curate pentru codul de producție
