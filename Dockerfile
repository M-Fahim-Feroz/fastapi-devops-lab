FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# system deps (psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# install deps first for cache
COPY api/requirements.txt .
RUN pip install --upgrade pip && pip install -r api/requirements.txt

# copy app
COPY . .

EXPOSE 8000
# adjust if your app lives somewhere else
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
