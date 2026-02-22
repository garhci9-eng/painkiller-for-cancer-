# Deployment Guide / 배포 가이드

## Local / 로컬 실행

```bash
pip install -r requirements.txt
streamlit run app.py
# → http://localhost:8501
```

---

## Docker

```bash
# 빌드 & 실행 / Build & run
docker compose up --build

# 백그라운드 / Background
docker compose up -d

# 중지 / Stop
docker compose down
```

---

## Streamlit Community Cloud (무료 / Free)

1. [share.streamlit.io](https://share.streamlit.io) 접속 / Go to Streamlit Cloud
2. GitHub 저장소 연결 / Connect GitHub repo
3. Main file path: `app.py`
4. Deploy 클릭 / Click Deploy
5. 자동으로 공개 URL 생성 / Public URL auto-generated

> ⚠️ RDKit은 Streamlit Cloud에서 `rdkit-pypi` 패키지 이름으로 설치됩니다.  
> `requirements.txt`의 `rdkit` → `rdkit-pypi==2023.9.5` 로 변경하세요.

---

## Render (무료 / Free)

```yaml
# render.yaml
services:
  - type: web
    name: cancer-drug-app
    env: docker
    dockerfilePath: ./Dockerfile
    envVars:
      - key: STREAMLIT_SERVER_PORT
        value: 8501
```

---

## Railway

```bash
railway login
railway init
railway up
```
