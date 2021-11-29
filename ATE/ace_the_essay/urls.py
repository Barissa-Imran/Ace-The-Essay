from django.urls import path
from django.views.generic import TemplateView
from .import views

urlpatterns = [
    path("", views.index, name="index"),
    path("whyus", views.whyus, name="whyus"),
    path("Termsofpayment", views.top, name="top"),
    path("FAQ", views.faq, name="faq"),
    path("Revisionpolicy", views.revision_policy, name="revision-policy"),
    path("Privacypolicy", views.privacy_policy, name="privacy-policy"),
    path("T&C", views.TC, name="TC"),
    path("HIW", views.HIW, name="HIW"),
]
