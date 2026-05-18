# UBB-AI 2025-2026 projects

## Metodologie de lucru

<details>

- Proiectele se pot realiza in echipa de maxim 4 persoane
- O echipa poate lucra la o singura tema de proiect. Un proiect poate fi ales de maxim 5 echipe, dar fiecare echipa va lucra independent.
- Echipele si temele vor fi comunicate cadrelor didactice care coordoneaza activitatea de laborator pana cel tarziu in **30 aprilie  2025**.
- Proiectele se vor incarca in acest [git](https://classroom.github.com/a/LESHiTyK). Fiecare proiect trebuie sa contina:
    - codul si explicatiile aferente (de ex. un notebook in care celulele de cod sa alterneze cu cele de explicatii) - organizate cat mai frumos 
    - un folder cu datele folosite 
    - o pagina de garda (readme) care sa contina informatii despre: 
        - echipa care a lucrat la proiect, 
        - problema abordata si 
        - un desen/schema care sa sugereze cat mai bine solutia propusa
    - cel putin cate 2 pull-request-uri (unul pentru fiecare etapa de predare) din partea fiecarui membru al echipei
- In saptamana 12 se vor prezenta, in cadrul orelor de laborator primele 2 etape (Definirea problemei si analiza datelor de intrare) si de vor incarca pe git materialele aferente
- In saptamana 14 se vor prezenta, in cadrul orelor de laborator, ultimele 2 etape (Dezvoltarea modelului si Imbunatatiri) si se vor incarca pe git materialele aferente
- In saptamana 14 (2 - 6 iunie) se vor incarca pe git filmulete scurte de prezentare a proiectelor realizate (doar de catre echipele care au obtinut cel putin 300p pana acum).
- Evaluare:
    - definirea problemei si analiza datelor de intrare - 200p
    - dezvoltarea unui model de AI si evaluarea performantei - 300p
    - imbunatatiri - 300p
    - teaser de prezentare a solutiei dezvoltate - 200p
        - ce problema rezolva proiectul (inputs, outputs)
        - ce tip de AI s-a folosit
        - ce performanta s-a obtinut
        - care sunt [SGD](https://unstats.un.org/wiki/display/SDGeHandbook/Home)-urile impactate de un astfel de proiect (motivati alegerea unuia sau mai multor obiective)
</details>

## Teme de proiect

Pentru oricare tema de proiect se va dezvolta un sistem inteligent bazat pe un agent AI care poate rezolva autonom problema descrisă, prin interpretarea instrucțiunilor în limbaj natural, planificarea pașilor necesari și utilizarea instrumentelor software pentru generarea unui rezultat final corect și relevant. Fiecare echipă va livra un prototip funcțional care demonstrează capacitatea agentului de a executa autonom un flux de lucru complex, folosind:
- modele ML/LLM studiate
- lanțuri de prompting
- un agent capabil să apeleze instrumente (tool use)
- tehnici de evaluare și testare

Proiectul trebuie să includă atât partea de inteligență artificială, cât și un modul minimal de interacțiune (CLI, API, UI simplă sau notebook interactiv).


<details>
    <summary> 1. CV Parsing and HR Assistant
    </summary>

#### Scop
Proiectarea și implementarea unui agent AI capabil să analizeze automat CV‑uri și descrieri de post, să extragă și să compare competențe relevante, să calculeze scoruri de potrivire și să furnizeze explicații și recomandări care sprijină reducerea timpului de recrutare și a influenței biasului în procesele de selecție. Proiectul nu are scopul de a automatiza complet deciziile de angajare, ci de a oferi suport decizional explicabil pentru utilizatorii umani.

#### Ideea de baza
În procesele de recrutare, personalul de HR se confruntă cu provocări semnificative în ceea ce privește trierea eficientă a CV-urilor și evaluarea candidaților pe baza calificărilor și experienței acestora. Volumul mare de aplicații primite pentru fiecare poziție este adesea copleșitor, ceea ce îngreunează identificarea celor mai potriviți candidați. Acest lucru duce la cicluri de angajare prelungite, posibila trecere cu vederea a unor candidați calificați și o încărcare suplimentară pentru personalul HR. În plus, procesul de revizuire manuală este predispus la bias și inconsistențe, ceea ce poate afecta calitatea generală a angajărilor și diversitatea bazei de candidați.

#### TODOlist
Dezvoltarea unui instrument de triere a CV-urilor bazat pe AI/ML care automatizează și standardizează evaluarea candidaților pentru a accelera angajările, a îmbunătăți calitatea potrivirii și a reduce biasul.

Caracteristici cheie și beneficii:
- Scor de potrivire a competențelor: Generează un scor procentual care compară fiecare CV cu descrierea postului, permițând HR-ului să prioritizeze rapid candidații cu potrivirea cea mai bună.
- Număr de entități/competențe: Extrage și contabilizează competențele și entitățile relevante pentru a oferi o imagine clară a calificărilor candidatului și pentru a identifica abilități comune sau unice în pool-ul de talente.
- Recomandări: Oferă sugestii pentru următorii pași (întrebări personalizate pentru interviu, semnale de alarmă, evaluări recomandate) pentru a eficientiza și standardiza deciziile de selecție.
- Analiza frazelor și a cuvintelor cheie: Detectează terminologia specifică industriei și expresiile relevante pentru a îmbunătăți acuratețea trierei și pentru a evita omiterea candidaților calificați.
- Reducerea biasului: Utilizează algoritmi obiectivi și standardizați pentru a minimiza biasul inconștient, sprijinind procese de angajare mai corecte și mai diverse.
- Dashboard ușor de utilizat: Vizualizează metrici (candidați triați, scoruri medii, top candidați) pentru decizii rapide și bazate pe date.
- Învățare continuă: Modelele ML se îmbunătățesc în timp folosind feedback și rezultate, menținând recomandările aliniate cu nevoile de angajare în evoluție.

#### Bibliografie

Devlin, J., Chang, M.‑W., Lee, K., & Toutanova, K. (2019). BERT: Pre‑training of deep bidirectional transformers for language understanding. Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics (NAACL‑HLT), 4171–4186. [link](https://doi.org/10.18653/v1/N19-1423)

Jurafsky, D., & Martin, J. H. (2023). Speech and language processing (3rd ed., draft). [link](https://web.stanford.edu/~jurafsky/slp3/)

Manning, C. D., Raghavan, P., & Schütze, H. (2008). Introduction to information retrieval. Cambridge University Press.

Reimers, N., & Gurevych, I. (2019). Sentence‑BERT: Sentence embeddings using Siamese BERT‑networks. Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing. [link](https://arxiv.org/abs/1908.10084)

</details>




