# Etapa 3 — Integrare & UI

**Responsabil:** 
**Scop:** Expune rezultatele din Etapa 2 printr-un API HTTP și un dashboard vizual accesibil oricărui utilizator.

---

## Flux

```
rezultat de la Etapa 2 (JSON complet)
    ↓ FastAPI
endpoint HTTP /analyze
    ↓ Streamlit
interfață vizuală în browser
    ↓ pytest
teste automate de validare
    ↓
→ utilizatorul final (HR-ul) vede rezultatul
```

---

## Pasul 1 — FastAPI (Backend / API)

**Scop:** primește CV-ul și JD-ul prin HTTP, apelează etapele 1+2, returnează JSON

```
Client trimite:
POST /analyze
{
  "cv_file": <fisier PDF>,
  "job_description": "Căutăm un Backend Engineer cu Python..."
}

Server răspunde:
{
  "scor": 91.5,
  "skills_potrivite": ["Python", "REST APIs"],
  "skills_lipsa": ["Kubernetes"],
  "recomandari": "...",
  "intrebari_interviu": [...],
  "red_flags": [...]
}
```

De ce e util: UI-ul, un alt sistem extern, sau profesorul pot apela API-ul direct fără să știe nimic despre codul din spate.

**Fișier:** `api/main.py`

---

## Pasul 2 — Streamlit (Dashboard vizual)

**Scop:** interfață grafică în browser — utilizatorul uploadează CV și lipește JD, vede rezultatul vizual

```
┌─────────────────────────────────────────┐
│  CV Analyzer — HR Assistant             │
│                                         │
│  [Upload CV]  cv_ion_popescu.pdf ✓      │
│                                         │
│  Job Description:                       │
│  ┌─────────────────────────────────┐    │
│  │ Căutăm Backend Engineer cu...   │    │
│  └─────────────────────────────────┘    │
│                                         │
│           [Analizează]                  │
└─────────────────────────────────────────┘
                ↓ după click
┌─────────────────────────────────────────┐
│  Scor potrivire:  91.5%                 │
│  ████████████████████░░░                │
│                                         │
│  ✅ Skills potrivite:                   │
│     Python, REST APIs                   │
│                                         │
│  ❌ Skills lipsă:                       │
│     Kubernetes                          │
│                                         │
│  🎁 Skills bonus (neceute):             │
│     Docker                              │
│                                         │
│  💬 Întrebări interviu:                 │
│  • Descrie o arhitectură REST API...    │
│  • Ai experiență cu K8s?               │
│                                         │
│  ⚠ Red flags:                          │
│  • Niciun proiect open-source          │
└─────────────────────────────────────────┘
```

**Fișier:** `ui/app.py`

---

## Pasul 3 — pytest (Testare automată)

**Scop:** verifică automat că nimic nu s-a stricat când cineva modifică codul

```python
def test_scor_in_interval_valid():
    rezultat = analyze(cv_sample, jd_sample)
    assert 0 <= rezultat["scor"] <= 100

def test_skills_lipsa_detectate():
    rezultat = analyze(cv_fara_kubernetes, jd_cu_kubernetes)
    assert "Kubernetes" in rezultat["skills_lipsa"]

def test_api_returneaza_200():
    response = client.post("/analyze", ...)
    assert response.status_code == 200
```

Rulezi `pytest` în terminal și în câteva secunde știi dacă totul funcționează.

**Fișiere:** `tests/test_parser.py`, `tests/test_matcher.py`

---

## Cum comunică toate etapele

```
HR-ul deschide browserul (Streamlit)
    → apasă Analizează
        → Streamlit apelează FastAPI  POST /analyze
            → FastAPI apelează Etapa 1  (parsare + NER + embeddings)
                → Etapa 1 trimite la Etapa 2  (matching + agent)
                    → Etapa 2 returnează JSON
                → FastAPI returnează JSON
            → Streamlit afișează vizual rezultatul
HR-ul vede scorul, skills-urile și recomandările
```

---

## Tehnologii

| Tehnologie | Rol |
|-----------|-----|
| FastAPI | Framework API HTTP |
| Uvicorn | Server ASGI pentru FastAPI |
| Streamlit | Dashboard vizual în browser |
| pytest | Testare automată |
