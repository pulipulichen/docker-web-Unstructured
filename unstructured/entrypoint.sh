#!/bin/bash

# uvicorn app:app --host 0.0.0.0 --port 8080 --workers ${UVICORN_WORKERS}
uvicorn app:app --host 0.0.0.0 --port 8080 --workers 1
# uvicorn app:app --host 0.0.0.0 --port 8080 --reload