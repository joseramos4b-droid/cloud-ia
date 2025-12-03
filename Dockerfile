FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=10000

CMD ["sh", "-c", "gunicorn --workers=1 --threads=2 --timeout=180 --bind 0.0.0.0:$PORT app:app"]
