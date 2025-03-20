# 使用 Python 官方映像檔
FROM python:3.11

# 設定工作目錄
WORKDIR /app

RUN apt update
RUN apt-get install -y libreoffice
# RUN apt install -y libgl1-mesa-glx

ENV UVICORN_WORKERS=1

# 複製需求檔案並安裝
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install python-multipart
RUN apt-get install -y unzip
# RUN pip install plistlib

# =================================================================

# =================================================================

# 啟動 FastAPI 伺服器
COPY entrypoint.sh /app/entrypoint.sh
CMD ["bash", "/app/entrypoint.sh"]
