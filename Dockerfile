FROM python:3.11-slim

WORKDIR /app

COPY . .

LABEL org.opencontainers.image.source=https://github.com/ewsmyth/vocobell

RUN apt-get update && apt-get install -y alsa-utils && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH=/app

EXPOSE 5665

CMD ["python", "main.py"]
