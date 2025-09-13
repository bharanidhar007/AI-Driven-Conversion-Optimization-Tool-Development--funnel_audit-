FROM python:3.11-slim
WORKDIR /code
COPY requirements.txt .
RUN apt-get update && apt-get install -y curl build-essential libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libx11-xcb1 libxcomposite1 libxrandr2 libxdamage1 libxss1 libasound2 libpangocairo-1.0-0 libxshmfence1 libgbm-dev libgtk-3-0 &&             pip install --no-cache-dir -r requirements.txt &&             playwright install chromium
COPY . .
ENV PYTHONUNBUFFERED=1
CMD ["gunicorn", "funnel_audit.wsgi:application", "-b", "0.0.0.0:8000"]
