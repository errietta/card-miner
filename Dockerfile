# Dockerfile for card-miner
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install fugashi[unidic-lite]
RUN pip install unidic-lite
RUN python -m unidic download

COPY .env .

VOLUME ["/app"]

ENV PYTHONUNBUFFERED=1

CMD ["python", "script.py"]
