# Etapa 1 — Date & NLP

**Responsabil:** 
**Scop:** Transformă fișiere brute (PDF/DOCX) în date structurate + vectori numerici gata de comparat.

---

## Flux

```
cv.pdf / cv.docx
    ↓ Parsare
text brut
    ↓ NER (spaCy)
dicționar structurat
    ↓ Embeddings (Sentence-BERT)
vectori numerici
    ↓
→ trimite la Etapa 2
```

---

## Pasul 1 — Parsare (PyPDF2, python-docx)

**Intră:** fișier `.pdf` sau `.docx`
**Iese:** string cu tot textul din CV

```python
# Exemplu output
"Ion Popescu\nSoftware Engineer cu 3 ani experiență\nSkills: Python, FastAPI, Docker\nEducație: UBB Cluj, Informatică, 2021"
```

**Fișier:** `ai_module/parser.py`

---

## Pasul 2 — NER / Extragere entități (spaCy)

**Intră:** textul brut
**Iese:** dicționar structurat cu câmpuri clare

```python
{
  "nume": "Ion Popescu",
  "titlu": "Software Engineer",
  "ani_experienta": 3,
  "skills": ["Python", "FastAPI", "Docker"],
  "educatie": "UBB Cluj, Informatică, 2021",
  "locatie": None
}
```

spaCy citește textul și recunoaște ce e skill, ce e instituție, ce e număr de ani — ca un cititor uman care scanează un CV.

**Fișier:** `ai_module/ner.py`

---

## Pasul 3 — Embeddings (Sentence-BERT, all-MiniLM-L6-v2)

**Intră:** liste de texte — ex. `["Python", "FastAPI", "Docker"]`
**Iese:** vectori numerici de 384 dimensiuni per element

```python
"Python"  → [0.23, -0.11, 0.87, 0.04, ...]   # 384 numere
"Django"  → [0.21, -0.09, 0.85, 0.06, ...]   # aproape identic cu Python
"Fotbal"  → [-0.54, 0.33, -0.12, 0.91, ...]  # complet diferit
```

**De ce?** Vectorii apropiați = texte cu sens similar. Asta permite matching-ului din Etapa 2 să înțeleagă că `FastAPI ≈ REST API framework` fără să fie același cuvânt.

**Fișier:** `ai_module/embeddings.py`

---

## Output final trimis către Etapa 2

```python
{
  "cv": {
    "skills": ["Python", "FastAPI", "Docker"],
    "skills_vector": [0.23, -0.11, 0.87, ...],
    "ani_experienta": 3,
    "educatie": "UBB Cluj, Informatică, 2021"
  },
  "jd": {
    "skills_cerute": ["Python", "REST APIs", "Kubernetes"],
    "skills_vector": [0.21, -0.08, 0.83, ...],
    "ani_experienta_minim": 2,
    "educatie_ceruta": "Informatică sau similar"
  }
}
```

---

## Tehnologii

| Tehnologie | Rol |
|-----------|-----|
| PyPDF2 | Extrage text din PDF |
| python-docx | Extrage text din DOCX |
| spaCy (`en_core_web_sm`) | NER — recunoaștere entități |
| sentence-transformers | Generare embeddings Sentence-BERT |
