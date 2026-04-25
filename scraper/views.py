import csv
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RegisterForm, ScrapeForm
from .models import ScrapeJob, ScrapedHeading, ScrapedLink
from .services import scrape_page

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'scraper/home.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = form.cleaned_data.get('email', '')
            user.save()
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'scraper/register.html', {'form': form})

@login_required
def dashboard(request):
    form = ScrapeForm()
    jobs = request.user.scrape_jobs.all()[:10]
    return render(request, 'scraper/dashboard.html', {'form': form, 'jobs': jobs})

@login_required
def scrape_create(request):
    if request.method != 'POST':
        return redirect('dashboard')

    form = ScrapeForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Please enter a valid URL.")
        return redirect('dashboard')

    url = form.cleaned_data['url']

    try:
        data = scrape_page(url)
        job = ScrapeJob.objects.create(
            user=request.user,
            url=data["final_url"],
            title=data["title"],
            meta_description=data["meta_description"],
            h1_count=data["h1_count"],
            h2_count=data["h2_count"],
            link_count=data["link_count"],
            status='success',
        )

        ScrapedHeading.objects.bulk_create([
            ScrapedHeading(job=job, tag=item["tag"], text=item["text"])
            for item in data["headings"]
        ])

        ScrapedLink.objects.bulk_create([
            ScrapedLink(job=job, text=item["text"], href=item["href"])
            for item in data["links"]
        ])

        messages.success(request, "Scraping completed successfully.")
        return redirect('job_detail', job_id=job.id)

    except ValueError as exc:
        job = ScrapeJob.objects.create(
            user=request.user,
            url=url,
            status='failed',
            error_message=str(exc),
        )
        messages.error(request, str(exc))
        return redirect('job_detail', job_id=job.id)

@login_required
def job_detail(request, job_id):
    job = get_object_or_404(ScrapeJob, id=job_id, user=request.user)
    return render(request, 'scraper/job_detail.html', {'job': job})

@login_required
def export_job_csv(request, job_id):
    job = get_object_or_404(ScrapeJob, id=job_id, user=request.user)

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="scrape_job_{job.id}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Type', 'Tag/Text', 'URL'])
    writer.writerow(['PAGE_TITLE', job.title, job.url])
    writer.writerow(['META_DESCRIPTION', job.meta_description, job.url])

    for heading in job.headings.all():
        writer.writerow(['HEADING', f"{heading.tag}: {heading.text}", job.url])

    for link in job.links.all():
        writer.writerow(['LINK', link.text, link.href])

    return response

@login_required
def export_all_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="scrape_history.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'URL', 'Title', 'Meta Description', 'H1 Count', 'H2 Count', 'Link Count', 'Status', 'Created At'])

    for job in request.user.scrape_jobs.all():
        writer.writerow([
            job.id,
            job.url,
            job.title,
            job.meta_description,
            job.h1_count,
            job.h2_count,
            job.link_count,
            job.status,
            job.created_at,
        ])

    return response
