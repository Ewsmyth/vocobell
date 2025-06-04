FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    alsa-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

LABEL org.opencontainers.image.source=https://github.com/ewsmyth/vocobell

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

EXPOSE 5665

CMD ["python", "main.py"]
