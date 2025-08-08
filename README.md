Video paraphrasing using gpt 4.0 completions endpoint

Video paraphrasing using gpt 4.0 completions endpoint

## Setup
- Create a virtualenv and install deps:
  - python3 -m venv .venv && source .venv/bin/activate
  - pip install -r requirements.txt
- Copy environment template and set values:
  - cp .env.example .env
  - Update DJANGO_SECRET_KEY (use a long random string)
  - Set USE_SQLITE=1 for quick local runs, or configure Postgres vars

## Environment variables (.env)
- DJANGO_SECRET_KEY
- DEBUG (0/1)
- ALLOWED_HOSTS (comma separated)
- USE_SQLITE (1 to use SQLite locally)
- POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT
- ASSEMBLYAI_API_KEY, OPENAI_API_KEY

## Run (SQLite)
- export $(cat .env | xargs); export USE_SQLITE=1
- python manage.py migrate
- python manage.py runserver 0.0.0.0:8000

## Run (Postgres)
- Ensure Postgres is running and env vars are set (USE_SQLITE not equal to 1)
- python manage.py migrate
- python manage.py runserver 0.0.0.0:8000

## Admin
- Create superuser: python manage.py createsuperuser
- Admin at /admin/

## Static
- App CSS and favicon are under static/

## Tests
- python manage.py test

## Notes
- This repo is the Django app located under backend/ai_blog_app in the workspace.
