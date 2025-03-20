#!/bin/bash

uvicorn main:app --host 0.0.0.0 --port 80 --workers 1
# uvicorn main:app --host 0.0.0.0 --port 8000 --reload
