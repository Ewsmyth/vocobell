FROM python:3.11-slim

WORKDIR /app

COPY . .

LABEL org.opencontainers.image.source=https://github.com/ewsmyth/vocobell

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app

EXPOSE 5665

CMD ["python", "main.py"]
