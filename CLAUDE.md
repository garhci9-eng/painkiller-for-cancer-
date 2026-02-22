# CLAUDE.md

This file provides context for AI assistants (Claude and others) working on this codebase.  
이 파일은 이 코드베이스에서 작업하는 AI 어시스턴트를 위한 컨텍스트를 제공합니다.

---

## Project Summary / 프로젝트 요약

**Cancer Pain Drug Discovery AI** is a Streamlit web application that screens non-opioid drug candidates for cancer pain using the ChEMBL public database, RDKit cheminformatics, and AI-based scoring.

암성 통증 비마약성 신약 후보 탐색 AI는 ChEMBL 공개 데이터베이스, RDKit 화학정보학, AI 기반 점수화를 사용하여 암성 통증에 대한 비오피오이드 신약 후보를 탐색하는 Streamlit 웹 앱입니다.

---

## Architecture / 아키텍처

```
app.py                  ← Entry point, Streamlit UI (5 tabs)
utils/
  chembl.py             ← ChEMBL API client + compound search
  molecules.py          ← RDKit descriptors + 2D image generation
  db.py                 ← SQLite CRUD (compounds, favorites, history)
data/
  compounds.db          ← Auto-created SQLite DB
```

---

## Key Design Decisions / 주요 설계 결정

- **No ML model training required**: scoring is rule-based (Lipinski + descriptor penalties) so the app works immediately without a training step
- **Graceful degradation**: if RDKit or ChEMBL client is unavailable, the app falls back to mock data / placeholder images — never crashes
- **SQLite over PostgreSQL**: keeps deployment simple; no external DB needed
- **Streamlit over Flask/FastAPI**: minimizes boilerplate for a research tool

---

## Non-Opioid Targets / 비마약성 타겟

| Target | ChEMBL ID | Mechanism |
|--------|-----------|-----------|
| Nav1.7 | CHEMBL4805 | Voltage-gated sodium channel, pain signal transmission |
| Nav1.8 | CHEMBL5163 | Peripheral sodium channel |
| TRPV1  | CHEMBL4794 | Capsaicin/heat receptor |
| P2X3   | CHEMBL3797 | ATP-gated ion channel |
| NK1    | CHEMBL1821 | Substance P receptor |

---

## Drug Score Formula / 약물 점수 공식

```
side_effect_score = penalties based on:
  MW > 500  → +0.20 | MW > 400  → +0.10
  LogP > 4  → +0.20 | LogP > 3  → +0.10
  TPSA < 40 → +0.15 | TPSA > 120 → +0.10
  ArRings > 4 → +0.15

drug_score = 1 - side_effect_score   (higher = better candidate)
```

---

## Common Tasks / 자주 하는 작업

**Add a new ChEMBL target:**
Edit `utils/chembl.py` → `TARGETS` dict and `TARGET_DESCRIPTIONS` dict.

**Change scoring weights:**
Edit `utils/molecules.py` → `side_effect_score()` function.

**Add a new UI tab:**
Edit `app.py` → add to `st.tabs([...])` and add `with tab_new:` block.

---

## License Constraint / 라이선스 제약

This project is **public interest only**. Do not add features that enable commercial use, monetization, or private profit. Any contribution must maintain this constraint.

이 프로젝트는 **공익 목적 전용**입니다. 상업적 사용, 수익화, 사적 이익을 가능하게 하는 기능을 추가하지 마세요.
