from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ScrapeJob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=1000)),
                ('title', models.CharField(blank=True, max_length=500)),
                ('meta_description', models.TextField(blank=True)),
                ('h1_count', models.PositiveIntegerField(default=0)),
                ('h2_count', models.PositiveIntegerField(default=0)),
                ('link_count', models.PositiveIntegerField(default=0)),
                ('status', models.CharField(choices=[('success', 'Success'), ('failed', 'Failed')], default='success', max_length=20)),
                ('error_message', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scrape_jobs', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='ScrapedHeading',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=10)),
                ('text', models.CharField(max_length=500)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='headings', to='scraper.scrapejob')),
            ],
        ),
        migrations.CreateModel(
            name='ScrapedLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=500)),
                ('href', models.URLField(blank=True, max_length=1000)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='scraper.scrapejob')),
            ],
        ),
    ]
