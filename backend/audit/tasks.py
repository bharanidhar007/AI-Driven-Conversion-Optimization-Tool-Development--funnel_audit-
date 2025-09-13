from celery import shared_task
from .models import Report, ReportDetail
from django.utils import timezone
from .scraper import scrape_page
from .extractor import run_extraction
from .openai_client import evaluate_with_openai
import traceback

@shared_task(bind=True, max_retries=1)
def enqueue_scrape_task(self, report_id, url, user_id):
    report = Report.objects.get(id=report_id)
    try:
        report.status = 'scraping'
        report.save()
        scraped = scrape_page(url)
        features = run_extraction(scraped)
        report.status = 'analyzing'
        report.save()
        ai_output = evaluate_with_openai(features)
        ReportDetail.objects.create(report=report, scraped=scraped, features=features, ai_analysis=ai_output)
        report.status = 'done'
        if isinstance(ai_output, dict):
            report.score = ai_output.get('score')
        report.finished_at = timezone.now()
        report.save()
    except Exception as e:
        report.status = 'failed'
        report.error = str(e) + "\n" + traceback.format_exc()
        report.save()
        raise self.retry(exc=e, countdown=30)
