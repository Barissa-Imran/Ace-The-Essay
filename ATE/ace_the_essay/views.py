from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib import messages
from .forms import ContactForm
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

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            # send email to support here
            messages.success(request, 'Your message has been sent succefully')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
    }
    return render(request, "ace_the_essay/contact.html", context)
