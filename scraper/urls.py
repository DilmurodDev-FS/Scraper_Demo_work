from django.contrib.auth import views as auth_views
from django.urls import path

from .views import (
    home, register_view, dashboard, scrape_create, job_detail,
    export_job_csv, export_all_csv
)

urlpatterns = [
    path('', home, name='home'),
    path('register/', register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='scraper/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('scrape/', scrape_create, name='scrape_create'),
    path('job/<int:job_id>/', job_detail, name='job_detail'),
    path('job/<int:job_id>/export/', export_job_csv, name='export_job_csv'),
    path('export/all/', export_all_csv, name='export_all_csv'),
]
