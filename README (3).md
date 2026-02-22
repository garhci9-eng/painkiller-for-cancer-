# 🔬 암성 통증 비마약성 신약 후보 탐색 AI
# 🔬 AI-Based Non-Opioid Drug Candidate Discovery for Cancer Pain

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red)](https://streamlit.io)
[![ChEMBL](https://img.shields.io/badge/Data-ChEMBL-orange)](https://www.ebi.ac.uk/chembl/)
[![License](https://img.shields.io/badge/License-Public_Interest_Only-green)](#license--라이선스)

---

## 개요 / Overview

**[KO]**
암성 통증(Cancer Pain)은 환자 삶의 질에 심각한 영향을 미칩니다. 현재 치료는 마약성 진통제(오피오이드)에 의존하는 경우가 많으나, 중독과 부작용 문제가 큽니다. 이 프로젝트는 공개 임상 데이터(ChEMBL)를 활용하여 마약성 의존 없이도 암성 통증에 효과적인 신약 후보 화합물을 AI로 탐색합니다.

**[EN]**
Cancer pain severely impacts patients' quality of life. Current treatments often rely on opioids, which carry significant risks of addiction and side effects. This project leverages open clinical data (ChEMBL) to discover non-opioid drug candidates effective against cancer pain using AI-powered screening.

---

## 주요 기능 / Features

| 기능 (KO) | Feature (EN) |
|-----------|--------------|
| ChEMBL 실시간 화합물 검색 | Real-time compound search via ChEMBL API |
| RDKit 분자 구조 2D 이미지 표시 | 2D molecular structure visualization (RDKit) |
| Lipinski Rule of Five 자동 필터링 | Automatic Lipinski Rule of Five filtering |
| AI 부작용 위험 점수 계산 | AI-based side-effect risk scoring |
| CSV 결과 다운로드 | CSV result export |
| SQLite 로컬 DB 저장 | Local SQLite database storage |
| 즐겨찾기 및 검색 기록 | Favorites & search history |
| SMILES 직접 입력 분석 | Direct SMILES input analysis |
| Docker 원클릭 실행 | One-command Docker deployment |

---

## 탐색 타겟 / Non-Opioid Pain Targets

| 타겟 / Target | 역할 (KO) | Role (EN) | ChEMBL ID |
|--------------|-----------|-----------|-----------|
| **Nav1.7** | 나트륨 채널 — 통증 신호 차단 | Sodium channel — blocks pain signal transmission | CHEMBL4805 |
| **Nav1.8** | 나트륨 채널 — 말초 통증 | Sodium channel — peripheral pain | CHEMBL5163 |
| **TRPV1**  | 캡사이신 수용체 — 암성/염증성 통증 | Capsaicin receptor — cancer/inflammatory pain | CHEMBL4794 |
| **P2X3**   | ATP 수용체 — 만성 통증 | ATP receptor — chronic pain | CHEMBL3797 |
| **NK1**    | 뉴로키닌 수용체 — 신경성 통증 | Neurokinin receptor — neuropathic pain | CHEMBL1821 |

---

## 실행 방법 / How to Run

### Python 직접 실행 / Run with Python

```bash
# 저장소 클론 / Clone
git clone https://github.com/YOUR_USERNAME/cancer-pain-drug-discovery.git
cd cancer-pain-drug-discovery

# 의존성 설치 / Install dependencies
pip install -r requirements.txt

# 앱 실행 / Run
streamlit run app.py
```

브라우저에서 `http://localhost:8501` 이 자동으로 열립니다.
Your browser will automatically open `http://localhost:8501`.

---

### Docker (권장 / Recommended)

```bash
# 빌드 후 실행 / Build & run
docker compose up --build

# 백그라운드 실행 / Background mode
docker compose up --build -d
```

`http://localhost:8501` 접속 / Open `http://localhost:8501`

---

## 프로젝트 구조 / Project Structure

```
cancer-pain-drug-discovery/
├── app.py                    # 메인 Streamlit 앱 / Main Streamlit app
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .streamlit/
│   └── config.toml           # 테마 설정 / Theme config
├── utils/
│   ├── chembl.py             # ChEMBL API 연동 / ChEMBL API integration
│   ├── molecules.py          # 분자 특성 + 이미지 / Molecular descriptors + images
│   └── db.py                 # SQLite DB 관리 / SQLite DB management
├── docs/
│   ├── architecture.md       # 아키텍처 / Architecture
│   └── deployment.md         # 배포 가이드 / Deployment guide
└── tests/
    ├── test_molecules.py
    └── test_db.py
```

---

## 필터링 기준 / Filtering Criteria

| 기준 (KO) | Criterion (EN) | 값 / Value |
|-----------|----------------|-----------|
| IC50 효능 임계값 | IC50 activity threshold | ≤ 1000 nM |
| 분자량 | Molecular weight | ≤ 500 Da |
| 지질 용해도 | Lipophilicity | LogP ≤ 5 |
| 수소결합 공여체 | H-bond donors | ≤ 5 |
| 수소결합 수용체 | H-bond acceptors | ≤ 10 |
| 약물 점수 | Drug score | ≥ 0.5 |

---

## 기술 스택 / Tech Stack

| 구성 / Component | 기술 / Technology |
|-----------------|------------------|
| 웹 앱 / Web App | Streamlit |
| 화학정보학 / Cheminformatics | RDKit |
| 데이터 수집 / Data | ChEMBL WebResource Client |
| 데이터 처리 / Processing | Pandas, NumPy |
| 데이터베이스 / Database | SQLite |
| 시각화 / Visualization | Matplotlib |
| 컨테이너 / Container | Docker |
| CI | GitHub Actions |

---

## 데이터 출처 / Data Sources

- [ChEMBL](https://www.ebi.ac.uk/chembl/) — 화합물-타겟 활성 데이터 / Compound-target activity data (CC BY-SA 3.0)
- [PubChem](https://pubchem.ncbi.nlm.nih.gov/) — 분자 구조 데이터 / Molecular structure data (Public Domain)
- [RDKit](https://www.rdkit.org/) — 화학정보학 라이브러리 / Cheminformatics library (BSD)

---

## License / 라이선스

**[KO]**
이 프로젝트는 **사용자 아이디어 50% + Claude AI (Anthropic) 아이디어 50%** 로 공동 창작되었습니다.

**[EN]**
This project was **co-created by the user (50%) and Claude AI by Anthropic (50%)**.

| | 허용 ✅ Permitted | 금지 ❌ Prohibited |
|--|------------------|------------------|
| **KO** | 학술 연구, 교육, 비영리, 공공보건 | 상업적 판매, 사적 이익 추구, 영리 사업화 |
| **EN** | Academic research, education, non-profit, public health | Commercial sale, private profit, monetization |

---

## 의료 고지 / Medical Disclaimer

**[KO]** 이 소프트웨어는 연구 참고용입니다. 실제 임상 또는 의약품 개발에 적용 시 반드시 전문 의료·약학 전문가의 검토를 받으세요.

**[EN]** This software is intended for research reference only. Any application to actual clinical practice or drug development must be reviewed by qualified medical and pharmaceutical professionals.
