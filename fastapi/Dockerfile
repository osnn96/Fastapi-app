# FastAPI Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY fastapi/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY fastapi/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
