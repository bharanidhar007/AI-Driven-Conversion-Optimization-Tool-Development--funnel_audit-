# Funnel Audit (React + Django) - Scaffold
This repository is a minimal scaffold for an AI-powered funnel auditing tool using React (Vite) + Django + Celery + Playwright + OpenAI.
It contains:
- backend/: Django project with audit app (DRF endpoints, Celery task stubs, Playwright scraper, extractor, OpenAI client)
- frontend/: Vite + React minimal app (simple UI to submit URLs and poll reports)
- docker-compose.yml to run services locally (Postgres, Redis, Django web, Celery worker, frontend)
-----------------------
Quickstart (local development):
1. Copy `.env` variables (create one) including OPENAI_API_KEY, DJANGO_SECRET, CELERY_BROKER_URL if needed.
2. Build and run: `docker-compose up --build`
3. Create a superuser and create a test user for JWT token, or implement signup endpoints.
4. Install Playwright browsers inside backend image as required (Dockerfile includes playwright install step).
Notes:
- This is a scaffold — do not run in production as-is. Secure secrets, configure HTTPS, and add rate-limiting and robots.txt honoring.


## Added features in scaffold
- JWT signup/login
- User Profile with credits & referral code
- Stripe webhook stub to add credits
- Frontend signup/login & profile display
- Production Dockerfile and deployment guide (PRODUCTION.md)
