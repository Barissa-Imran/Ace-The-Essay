from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from users import views as user_views

# app_name = 'users'

urlpatterns = [

    # user auth urls
    path("login/", auth_views.LoginView.as_view(template_name='users/login.html'), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name='users/logout.html'), name="logout"),
    path("password-reset/", auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html'),
        name="password_reset"),
    path("password-reset-confirm/<uidb64>/<token>",
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'),
         name="password_reset_confirm"),
    path("password-reset/done", auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'),
        name="password_reset_done"),
    path("password-reset-complete", auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'),
        name="password_reset_complete"),

    # Applicant page urls
    path("apply", user_views.apply, name="apply"),
    path("applicant/application", user_views.application, name="application"),
    path("applicant/application-task",
         user_views.application_task, name="application_task"),

    # admin landing page
    path("admin-landing", user_views.admin_landing, name="admin_landing"),
    # Project detail view
    path("project/<slug>", user_views.ProjectDetailView.as_view(), name="project_detail"),
    path("client/project-new/", user_views.ProjectCreateView.as_view(), name="project_create"),
    # Project update view
    path("project/<slug>/update", user_views.ProjectUpdateView.as_view(), name="project_update"),
    # url(r'^saveForm/$', user_views.BidFormView.as_view(), name='form'),
    # search results url
    path("search/results/", user_views.search_results, name="search_results"),

    # Writer Dashboard pages urls
    path("writer", user_views.writer, name="writer"),
    path("writer/projects", user_views.projects, name="projects"),
    path("writer/bids", user_views.writer_bids, name="writer_bids"),
    path("writer/invoices", user_views.invoices, name="invoices"),
    path("writer/reports", user_views.reports, name="reports"),
    path("writer/settings", user_views.settings, name="settings"),
    path("writer/library", user_views.library, name="library"),


    # Client Dashboard pages urls
    path("client", user_views.client, name="client"),
    path("client/place-order", user_views.place_order, name="place_order"),
    path("client/invoices", user_views.client_invoices, name="client_invoices"),
    path("client/projects", user_views.client_projects, name="client_projects"),
    path("client/bids", user_views.client_bids, name="client_bids"),
    path("client/reports", user_views.client_reports, name="client_reports"),
    path("client/settings", user_views.client_settings, name="client_settings"),

    # path("client/projects", user_views.ClientProjectsListView.as_view(), name='client_projects'),
]
