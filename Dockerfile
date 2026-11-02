# PasameEso container image (DEP-06)
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /srv/pasameeso

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

# Database and uploads live in instance/, mounted as a volume so they survive rebuilds.
VOLUME ["/srv/pasameeso/instance"]

EXPOSE 8000

# Create the database on first start only, then serve with gunicorn.
CMD ["sh", "-c", "[ -f instance/pasameeso.sqlite ] || flask --app app init-db; gunicorn --bind 0.0.0.0:8000 --workers 3 'app:create_app()'"]
