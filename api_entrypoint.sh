cd /app/

uvicorn src.app:app --reload --workers 1 --host 0.0.0.0 --port 5000
