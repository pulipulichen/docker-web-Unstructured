# FROM unstructuredio/unstructured:0.14.8
FROM pudding/docker-web:docker-document-semantic-database-unstructured-20250316-1358

RUN mkdir -p /var/
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# RUN pip install redis

EXPOSE 8080

ENV UVICORN_WORKERS=8

# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "${UVICORN_WORKERS}"]
COPY entrypoint.sh /app/entrypoint.sh
CMD ["bash", "entrypoint.sh"]

USER root
RUN mkdir -p /uploads/
RUN chmod 777 /uploads/
USER notebook-user

COPY app.py /app/app.py


