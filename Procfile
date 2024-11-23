web: gunicorn app:app
web: uvicorn main:app --host 0.0.0.0 --port $PORT
web: ./setup.sh && gunicorn main:app

