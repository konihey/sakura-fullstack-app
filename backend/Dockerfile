FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && apt-get update \
    && apt-get install -y netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# DBの起動を待ってからアプリを起動
CMD sh -c 'while ! nc -z db 5432; do sleep 1; done; python app.py'