from django.urls import path
from django.views.generic import TemplateView
from .import views

urlpatterns = [
    path("", views.index, name="index"),
    path("whyus", views.whyus, name="whyus"),
    path("Terms-of-payment", views.top, name="top"),
    path("FAQ", views.faq, name="faq"),
    path("Revision-policy", views.revision_policy, name="revision-policy"),
    path("Privacy-policy", views.privacy_policy, name="privacy-policy"),
    path("T&C", views.TC, name="TC"),
    path("How-it-works", views.HIW, name="HIW"),
    path("contact-us", views.contact, name="contact"),
]
