from django.urls import path
from writer import views as writer_views

urlpatterns = [
    
    # Applicant page urls
    path("apply", writer_views.apply, name="apply"),
    path("applicant/application", writer_views.application, name="application"),
    path("applicant/application-task",
         writer_views.application_task, name="application_task"),

    # Writer Dashboard pages urls
    path("writer", writer_views.writer, name="writer"),
    path("writer/projects", writer_views.projects, name="projects"),
    path("writer/bids", writer_views.writer_bids, name="writer_bids"),
    path("writer/invoices", writer_views.invoices, name="invoices"),
    path("writer/reports", writer_views.reports, name="reports"),
    path("writer/settings", writer_views.settings, name="settings"),
    path("writer/library", writer_views.library, name="library"),
]
