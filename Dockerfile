FROM python:3.11-slim

# 시스템 의존성 (RDKit 빌드에 필요)
RUN apt-get update && apt-get install -y \
    libxrender1 libxext6 libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 의존성 먼저 설치 (캐시 최적화)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 앱 복사
COPY . .

# data 폴더 생성 (DB 저장용)
RUN mkdir -p /app/data

# Streamlit 설정
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
