FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV TRANSFORMERS_CACHE=/app/model_cache

ENTRYPOINT ["python", "main.py"]
