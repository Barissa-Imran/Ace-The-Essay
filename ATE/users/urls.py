from django.urls import path
from django.contrib.auth import views as auth_views
from users import views as user_views

urlpatterns = [
    path("apply", user_views.apply, name="apply"),

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

    # Landing pages
    path("application", user_views.application, name="application"),
    path("client", user_views.client, name="client"),

    # Writer Dashboard pages urls
    path("writer", user_views.writer, name="writer"),
    path("projects", user_views.projects, name="projects"),
    path("invoices", user_views.invoices, name="invoices"),
    path("reports", user_views.reports, name="reports"),
    path("settings", user_views.settings, name="settings"),
    path("settings/profile", user_views.profile, name="profile"),
]
