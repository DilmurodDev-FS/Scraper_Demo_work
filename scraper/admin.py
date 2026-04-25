from django.contrib import admin
from .models import ScrapeJob, ScrapedHeading, ScrapedLink

class ScrapedHeadingInline(admin.TabularInline):
    model = ScrapedHeading
    extra = 0

class ScrapedLinkInline(admin.TabularInline):
    model = ScrapedLink
    extra = 0

@admin.register(ScrapeJob)
class ScrapeJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'url', 'status', 'h1_count', 'h2_count', 'link_count', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('url', 'title')
    inlines = [ScrapedHeadingInline, ScrapedLinkInline]
