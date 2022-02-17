from django.urls import path
from client import views as client_views

urlpatterns = [
    path("project/<slug>", client_views.ProjectDetailView.as_view(),
         name="project_detail"),

    # Client Dashboard pages urls
    path("client", client_views.client, name="client"),
    # path("client/place-order", client_views.place_order, name="place_order"),
    path("client/place-order",
         client_views.ProjectCreateView.as_view(), name="place_order"),
    path("project/<slug>/update",
         client_views.ProjectUpdateView.as_view(), name="project_update"),
    path("project/<slug>/delete",
         client_views.ProjectDeleteView.as_view(), name="project_delete"),
    path("order/deleted", client_views.project_deleted, name="project_deleted"),
    path("client/invoices", client_views.client_invoices, name="client_invoices"),
    path("client/projects", client_views.client_projects, name="client_projects"),
    path("client/bids", client_views.client_bids, name="client_bids"),
    path("client/reports", client_views.client_reports, name="client_reports"),
    path("client/settings", client_views.client_settings, name="client_settings"),
]
