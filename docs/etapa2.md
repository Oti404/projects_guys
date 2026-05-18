# Etapa 2 — Matching & Agent AI

**Responsabil:** 
**Scop:** Compară CV-ul cu Job Description-ul, calculează scorul de potrivire cu explicații, și generează recomandări prin agent AI.

---

## Flux

```
cv_vector + jd_vector (de la Etapa 1)
    ↓ Similaritate cosinus
scor brut per categorie
    ↓ Formulă ponderată
scor_final + skills_potrivite + skills_lipsă
    ↓ Agent Azure OpenAI (tool use)
recomandări + întrebări interviu + red flags
    ↓
→ trimite la Etapa 3
```

---

## Pasul 1 — Similaritate cosinus

**Intră:** vectorii din Etapa 1
**Iese:** număr între 0 și 1 reprezentând cât de similar e sensul

```
cv_skills_vector  →  •
                      \
                       \  unghi mic = texte similare
                        •  ← jd_skills_vector

rezultat: 0.87  (87% similar semantic)
```

Dacă CV-ul zice `FastAPI` și JD-ul cere `REST API framework` → vectorii sunt apropiați → scor mare, chiar dacă cuvintele sunt diferite.

**Fișier:** `ai_module/matcher.py`

---

## Pasul 2 — Formulă ponderată + Explicabilitate

**Intră:** scoruri cosinus per categorie
**Iese:** scor final + detalii despre ce a prins și ce a lipsit

```python
scor_final = (skills 50%) + (experienta 30%) + (educatie 20%)
           = (0.87 × 0.5) + (1.0 × 0.3) + (0.9 × 0.2)
           = 0.435 + 0.30 + 0.18
           = 0.915 → 91.5%

{
  "scor": 91.5,
  "skills_potrivite": ["Python", "REST APIs"],   # FastAPI ≈ REST APIs
  "skills_lipsa": ["Kubernetes"],                # nu apare în CV
  "skills_bonus": ["Docker"]                     # în CV dar neceut în JD
}
```

Ponderile (50/30/20) sunt configurabile — pot fi ajustate în funcție de tipul postului.

**Fișier:** `ai_module/matcher.py`

---

## Pasul 3 — Agent AI cu Tool Use (Azure OpenAI)

**Intră:** instrucțiune în limbaj natural + CV + JD
**Iese:** analiză completă generată de LLM

Agentul primește o cerere și **decide singur ce funcții să apeleze și în ce ordine:**

```
Instrucțiune: "Analizează acest CV pentru postul de Backend Engineer"

Agent gândește și execută:
  1. parse_cv(file)                        → structură CV
  2. parse_job_description(text)           → cerințe JD
  3. calculate_match(cv_data, jd_data)     → scor + detalii
  4. generate_recommendations(...)         → recomandări finale
```

Fiecare tool e o funcție Python normală. Agentul știe ce tooluri are disponibile și alege când și cum le apelează.

**Output final al agentului:**

```
Scor potrivire: 91.5%

Skills potrivite:  Python ✓, REST APIs ✓ (via FastAPI)
Skills lipsă:      Kubernetes — recomand să întrebi candidatul
                   dacă are experiență cu container orchestration

Întrebări recomandate pentru interviu:
  1. Descrie o arhitectură REST API pe care ai construit-o
  2. Ai experiență cu orchestrarea containerelor (K8s, ECS)?
  3. Cum ai gestionat scalabilitatea în proiectele cu FastAPI?

Red flags:
  ⚠ Niciun proiect open-source menționat
  ⚠ Gap de 8 luni în CV între 2022-2023
```

**Fișier:** `ai_module/agent.py`

---

## Toolurile agentului

| Tool | Intrare | Ieșire |
|------|---------|--------|
| `parse_cv(file_path)` | cale fișier PDF/DOCX | dicționar structurat CV |
| `parse_job_description(text)` | text JD | dicționar cerințe |
| `calculate_match(cv, jd)` | cele două dicționare | scor + skills potrivite/lipsă |
| `generate_recommendations(cv, jd, scor)` | toate de mai sus | întrebări interviu + red flags |

---

## Output final trimis către Etapa 3

```python
{
  "scor": 91.5,
  "skills_potrivite": ["Python", "REST APIs"],
  "skills_lipsa": ["Kubernetes"],
  "skills_bonus": ["Docker"],
  "recomandari": "Candidat puternic, verificați experiența K8s",
  "intrebari_interviu": [
    "Descrie o arhitectură REST API pe care ai construit-o",
    "Ai experiență cu orchestrarea containerelor?",
    "Cum ai gestionat scalabilitatea în FastAPI?"
  ],
  "red_flags": [
    "Niciun proiect open-source menționat",
    "Gap de 8 luni în CV între 2022-2023"
  ]
}
```

---

## Tehnologii

| Tehnologie | Rol |
|-----------|-----|
| scikit-learn | Calcul similaritate cosinus |
| Azure OpenAI (GPT-4o mini) | LLM pentru agent și recomandări |
| python-dotenv | Citire cheie API din `.env` |
