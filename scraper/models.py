from django.conf import settings
from django.db import models

class ScrapeJob(models.Model):
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='scrape_jobs')
    url = models.URLField(max_length=1000)
    title = models.CharField(max_length=500, blank=True)
    meta_description = models.TextField(blank=True)
    h1_count = models.PositiveIntegerField(default=0)
    h2_count = models.PositiveIntegerField(default=0)
    link_count = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='success')
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.url} - {self.status}"


class ScrapedLink(models.Model):
    job = models.ForeignKey(ScrapeJob, on_delete=models.CASCADE, related_name='links')
    text = models.CharField(max_length=500, blank=True)
    href = models.URLField(max_length=1000, blank=True)

    def __str__(self):
        return self.text or self.href


class ScrapedHeading(models.Model):
    job = models.ForeignKey(ScrapeJob, on_delete=models.CASCADE, related_name='headings')
    tag = models.CharField(max_length=10)
    text = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.tag}: {self.text[:60]}"
