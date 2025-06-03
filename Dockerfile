FROM --platform=linux/arm64 python:3.11-slim

WORKDIR /app

COPY . /app

LABEL org.opencontainers.image.source https://github.com/ewsmyth/vocobell

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5665

CMD ["python", "main.py"]
