from django.shortcuts import render
from django.views.generic import TemplateView, ListView

class HomeView(TemplateView):
    template_name = "core.html"

def index(request):
    return render(request, "ace_the_essay/core.html")

def whyus(request):
    return render(request, "ace_the_essay/whyus.html")


def top(request):
    return render(request, "ace_the_essay/top.html")


def faq(request):
    return render(request, "ace_the_essay/faq.html")


def revision_policy(request):
    return render(request, "ace_the_essay/revision-policy.html")


def privacy_policy(request):
    return render(request, "ace_the_essay/privacy-policy.html")


def TC(request):
    return render(request, "ace_the_essay/TC.html")

def HIW(request):
    return render(request, "ace_the_essay/hiw.html")

