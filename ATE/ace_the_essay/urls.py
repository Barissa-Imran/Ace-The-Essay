from django.urls import path
from django.views.generic import TemplateView
from .import views

urlpatterns = [
    path("", views.indexView.as_view(), name="index"),
    path("whyus", views.whyusView.as_view(), name="whyus"),
    path("Terms-of-payment", views.topView.as_view(), name="top"),
    path("FAQ", views.faqView.as_view(), name="faq"),
    path("Revision-policy", views.revisionPolicyView.as_view(), name="revision-policy"),
    path("Privacy-policy", views.privacyPolicyView.as_view(), name="privacy-policy"),
    path("T&C", views.termsView.as_view(), name="TC"),
    path("How-it-works", views.HIWView.as_view(), name="HIW"),
    path("contact-us", views.contactView.as_view(), name="contact"),
]
