# Scraper Dashboard Django

Portfolio-ready Django web scraping project.

## Features
- Login / register
- URL scraping
- Extracts title, meta description, H1/H2 headings, links
- Saves scrape history per user
- CSV export for single job and full history
- Render deploy config included

## Local run
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open:
- Home: http://127.0.0.1:8000/
- Dashboard: http://127.0.0.1:8000/dashboard/
- Admin: http://127.0.0.1:8000/admin/

## Render
Build Command:
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

Start Command:
```bash
gunicorn scraperdash.wsgi:application
```

Environment Variables:
```text
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-service-name.onrender.com
```

## Important
Use this tool only on websites you are allowed to access.
