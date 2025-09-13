import uuid
from django.db import models
from django.contrib.auth import get_user_model
import secrets

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    credits = models.IntegerField(default=1)
    referral_code = models.CharField(max_length=32, unique=True, blank=True)
    referred_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='referred_users')

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = secrets.token_urlsafe(8)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} profile'

class Report(models.Model):
    STATUS_CHOICES = [('queued','Queued'),('scraping','Scraping'),('analyzing','Analyzing'),('done','Done'),('failed','Failed')]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    url = models.URLField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='queued')
    score = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    error = models.TextField(null=True, blank=True)

class ReportDetail(models.Model):
    report = models.OneToOneField(Report, on_delete=models.CASCADE, related_name='detail')
    scraped = models.JSONField(null=True, blank=True)
    features = models.JSONField(null=True, blank=True)
    ai_analysis = models.JSONField(null=True, blank=True)
