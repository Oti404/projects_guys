# Script Teaser — AI HR Assistant

**Durată recomandată:** 2–3 minute  
**Format:** screen recording cu voiceover

---

## [0:00 – 0:20] Hook — Problema

> "Imaginați-vă că primiți 300 de CV-uri pentru un singur post. Le citiți manual timp de o săptămână. La final, poate ați ratat cel mai bun candidat — din cauza oboselii, nu a lipsei de calificare."

*[Arată un folder plin cu PDF-uri sau un inbox supraaglomerat]*

---

## [0:20 – 0:50] Ce face sistemul nostru — Input/Output

> "AI HR Assistant rezolvă exact această problemă. HR-ul încarcă CV-ul candidatului și lipește descrierea postului."

*[Demo: deschide aplicația Angular, arată interfața]*

> "În câteva secunde, sistemul returnează:"
> - Un **scor de potrivire** (ex: 78%)
> - **Skill-urile găsite** în CV față de cerințe
> - **Skill-urile lipsă** — ce să verifici la interviu
> - **3 întrebări personalizate** pentru interviu
> - **Red flags** detectate automat

*[Arată rezultatul pe ecran cu toate câmpurile completate]*

---

## [0:50 – 1:20] Ce tip de AI am folosit

> "Sistemul combină trei straturi de inteligență artificială:"

1. **NLP clasic** — spaCy pentru extragerea entităților din CV (skills, experiență, educație)
2. **Semantic embeddings** — modelul Sentence-BERT `all-MiniLM-L6-v2` transformă textul în vectori de 384 dimensiuni, permițând matching semantic: `FastAPI ≈ REST API framework`, chiar dacă cuvintele sunt diferite
3. **LLM generativ** — Azure OpenAI GPT-4o mini cu Structured Outputs (JSON Schema strict) pentru recomandări calitative și întrebări de interviu

> "Scorul final e calculat printr-o formulă ponderată: 50% skills, 30% experiență, 20% educație."

---

## [1:20 – 1:50] Performanța obținută

> "Am antrenat și validat pe un dataset de **2.484 CV-uri reale** din 24 de domenii profesionale."

Metrici cheie:
- **Dataset:** 2.484 CV-uri, 24 categorii (IT, Finance, Healthcare, Engineering etc.)
- **Lungime medie CV:** 811 cuvinte (mediană: 757 cuvinte)
- **Prag clasificare:** `strong_match` ≥ 85% | `good_match` ≥ 70% | `partial_match` ≥ 50% | `weak_match` < 50%
- **Similaritate semantică:** cosinus pe vectori Sentence-BERT — detectează echivalențe terminologice fără reguli manuale
- **Output garantat:** schema JSON strict blochează LLM-ul să returneze date invalide (0 erori de parsing în testare)

---

## [1:50 – 2:20] SDG-uri impactate

> "Proiectul nostru contribuie direct la trei Obiective de Dezvoltare Durabilă ale ONU:"

**SDG 8 — Muncă decentă și creștere economică**
> Reducem timpul de screening de la zile la secunde, eliberând HR-ul pentru munca cu adevărat umană: interviurile și decizia finală.

**SDG 10 — Inegalități reduse**
> Evaluarea standardizată reduce prejudecățile inconștiente (bias de gen, etnie, vârstă) care apar în screening-ul manual — toți candidații sunt evaluați după același set de criterii obiective.

**SDG 9 — Industrie, inovație și infrastructură**
> Demonstrăm cum AI generativ + NLP clasic pot fi integrate într-un sistem explicabil și responsabil, nu o cutie neagră.

---

## [2:20 – 2:40] Concluzie

> "AI HR Assistant nu înlocuiește recrutorul uman — îi oferă un copilot rapid, consistent și explicabil."
> "Codul sursă, datele și documentația completă sunt disponibile pe GitHub."

*[Arată repo-ul / README-ul]*

---

## Note pentru filmare

- Rulați `uvicorn api.main:app` înainte de a porni înregistrarea
- Folosiți un CV de test din `data/cv_samples.txt`
- Rezoluție recomandată: 1920×1080, voiceover separat editat
