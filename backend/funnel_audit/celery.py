import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'funnel_audit.settings')
app = Celery('funnel_audit')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
