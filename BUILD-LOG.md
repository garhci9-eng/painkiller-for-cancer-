# Build Log / 개발 일지

Development history of the Cancer Pain Drug Discovery AI.  
암성 통증 비마약성 신약 탐색 AI 개발 과정 기록.

---

## v1.0.0 — 2025-02-22

### Session 1 — Concept & Planning / 컨셉 및 기획

**[KO]**
- 문제 정의: 암성 통증 환자의 오피오이드 의존 문제
- 해결 방향: 공개 임상 데이터 기반 비마약성 신약 후보 AI 탐색
- 타겟 선정: Nav1.7, Nav1.8, TRPV1, P2X3, NK1
- 기술 스택 결정: Python + Streamlit + ChEMBL + RDKit + SQLite

**[EN]**
- Problem: opioid dependency in cancer pain management
- Solution direction: AI screening of non-opioid candidates using public clinical data
- Target selection: Nav1.7, Nav1.8, TRPV1, P2X3, NK1
- Tech stack: Python + Streamlit + ChEMBL + RDKit + SQLite

---

### Session 2 — Core Implementation / 핵심 구현

**[KO]**
- `utils/chembl.py`: ChEMBL API 연동, IC50 기반 화합물 검색
- `utils/molecules.py`: RDKit 분자 특성 계산 + 2D 이미지 생성, graceful fallback
- `utils/db.py`: SQLite CRUD (화합물 저장, 즐겨찾기, 검색 기록)
- `app.py`: Streamlit 5탭 UI (후보 탐색, SMILES 분석, 저장, 즐겨찾기, 기록)
- Lipinski Rule of Five 자동 필터링
- AI 부작용 위험 점수 공식 설계

**[EN]**
- `utils/chembl.py`: ChEMBL API integration, IC50-based compound search
- `utils/molecules.py`: RDKit molecular descriptor calculation + 2D image generation
- `utils/db.py`: SQLite CRUD (compound storage, favorites, search history)
- `app.py`: 5-tab Streamlit UI
- Lipinski Rule of Five automatic filtering
- AI side-effect risk scoring formula

---

### Session 3 — Polish & GitHub Prep / 마무리 및 GitHub 준비

**[KO]**
- Docker + docker-compose 지원 추가
- `.streamlit/config.toml` 테마 설정
- GitHub Actions CI 파이프라인
- 이중 언어(한국어/영어) README
- CHANGELOG, AUTHORS, ATTRIBUTION, SECURITY, CLAUDE.md 작성
- 공익 라이선스 명시

**[EN]**
- Docker + docker-compose support
- Streamlit theme configuration
- GitHub Actions CI pipeline
- Bilingual (Korean/English) README
- CHANGELOG, AUTHORS, ATTRIBUTION, SECURITY, CLAUDE.md
- Public interest license

---

## Co-Creation Note / 공동 창작 메모

This project was built through a conversation-driven development process between a user and Claude AI (Anthropic). The user provided the domain concept, clinical direction, and use-case requirements. Claude designed and implemented the full software architecture and codebase.

이 프로젝트는 사용자와 Claude AI(Anthropic) 간의 대화 기반 개발 과정을 통해 만들어졌습니다. 사용자가 도메인 컨셉, 임상 방향, 사용 사례 요구사항을 제공하고, Claude가 전체 소프트웨어 아키텍처와 코드베이스를 설계·구현하였습니다.
