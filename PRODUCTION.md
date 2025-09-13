# Production Deployment Guide (overview)

This document outlines recommended steps to deploy the Funnel Audit app in production.

1. Use Postgres for DATABASES. Example in Docker Compose / Kubernetes secret.
2. Use Redis for Celery broker. Run multiple worker replicas with limited concurrency (1-2 browsers per worker).
3. Store screenshots and large artifacts in S3 (or equivalent). Serve static files via CDN.
4. Secure environment variables:
   - DJANGO_SECRET
   - OPENAI_API_KEY
   - STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET
   - DATABASE_URL
   - CELERY_BROKER_URL
5. Use the provided backend/Dockerfile.prod for building container images. Run containers as non-root.
6. Configure gunicorn with multiple workers and set timeout appropriately for longer scraping tasks.
7. Use a load balancer (e.g., ALB/NGINX) and ensure HTTPS termination.
8. Implement rate limiting on API endpoints to avoid abuse.
9. Verify and validate webhook signatures from Stripe. Do not trust payloads blindly.
10. Use a secrets manager for production (AWS Secrets Manager, HashiCorp Vault).
11. Monitoring & Logging: enable Sentry, Prometheus, and structured logs.
12. Compliance: respect robots.txt and do not scrape password-protected content.

Example: Kubernetes deployment (outline)
- Deploy backend as Deployment & Service
- Use HorizontalPodAutoscaler for workers and backend
- Run Playwright in sidecar or dedicated worker pods with appropriate resource requests/limits
- Use PersistentVolume for Postgres
