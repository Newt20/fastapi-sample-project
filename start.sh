#!/bin/sh

if [ "$SERVICE_TYPE" = "fastapi" ]; then
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
elif [ "$SERVICE_TYPE" = "celery" ]; then
    celery -A tasks.celery_app worker --loglevel=info
else
    echo "SERVICE_TYPE not set or invalid. Using default (both services)."
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
    celery -A tasks.celery_app worker --loglevel=info
fi