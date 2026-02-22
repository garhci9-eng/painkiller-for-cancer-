# Architecture / 아키텍처

## System Overview / 시스템 개요

```
┌─────────────────────────────────────────────────────┐
│                  Streamlit Web App                   │
│                     (app.py)                         │
│                                                      │
│  Tab 1: Search  │ Tab 2: SMILES │ Tab 3: Saved      │
│  Tab 4: Favs    │ Tab 5: History                     │
└────────┬─────────────────┬──────────────┬───────────┘
         │                 │              │
         ▼                 ▼              ▼
┌─────────────┐  ┌──────────────┐  ┌───────────────┐
│  chembl.py  │  │ molecules.py │  │    db.py      │
│             │  │              │  │               │
│ ChEMBL API  │  │ RDKit        │  │ SQLite DB     │
│ IC50 search │  │ Descriptors  │  │ compounds     │
│ + filtering │  │ + 2D images  │  │ favorites     │
└──────┬──────┘  └──────────────┘  │ history       │
       │                           └───────────────┘
       ▼
┌─────────────┐
│  ChEMBL DB  │
│  (public)   │
│  ebi.ac.uk  │
└─────────────┘
```

---

## Data Flow / 데이터 흐름

1. User selects target + IC50 threshold in sidebar
2. `chembl.py` queries ChEMBL API → returns raw compound list
3. `molecules.py` calculates descriptors (MW, LogP, TPSA, etc.) for each compound
4. Lipinski filter applied → non-drug-like molecules removed
5. Side-effect score calculated → `drug_score = 1 - side_effect_score`
6. Results sorted by `drug_score` descending
7. `db.py` saves results to SQLite
8. UI renders top-N compound cards with 2D structure images + charts

---

## Scoring Formula / 점수 계산 공식

```python
side_effect_score = 0.0

if MW > 500:    score += 0.20
elif MW > 400:  score += 0.10

if LogP > 4:    score += 0.20
elif LogP > 3:  score += 0.10

if TPSA < 40:   score += 0.15
elif TPSA > 120: score += 0.10

if ArRings > 4: score += 0.15

drug_score = 1 - min(side_effect_score, 1.0)
```

---

## Database Schema / DB 스키마

```sql
-- 검색된 화합물
CREATE TABLE compounds (
    id              INTEGER PRIMARY KEY,
    chembl_id       TEXT UNIQUE,
    smiles          TEXT,
    target          TEXT,
    ic50_nM         REAL,
    mw, logp, hbd, hba, tpsa, rot_bonds  REAL/INTEGER,
    lipinski_pass   INTEGER,
    drug_score      REAL,
    side_effect_score REAL,
    saved_at        TEXT
);

-- 즐겨찾기
CREATE TABLE favorites (
    id        INTEGER PRIMARY KEY,
    chembl_id TEXT UNIQUE,
    note      TEXT,
    saved_at  TEXT
);

-- 검색 기록
CREATE TABLE search_history (
    id           INTEGER PRIMARY KEY,
    target       TEXT,
    ic50_max     REAL,
    result_count INTEGER,
    searched_at  TEXT
);
```
