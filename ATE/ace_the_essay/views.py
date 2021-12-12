from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib import messages
from django.core.mail import send_mail
from decouple import config
from django.template.loader import render_to_string
from .forms import ContactForm


# class HomeView(TemplateView):
#     template_name = "core.html"


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

# contact page view


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # send email to support here making sure the message is not saved before being sent to support
            try:
                form.save()
                name = form.cleaned_data.get('name')
                email = form.cleaned_data.get('email')
                subject = form.cleaned_data.get('subject')
                message = form.cleaned_data.get('message')

                context = {
                    'name': name,
                    'email': email,
                    'subject': subject,
                    'message': message
                }

                msg_plain = render_to_string('mail/contact.txt', context)
                send_mail(
                    'CONTACT US PAGE',
                    msg_plain,
                    config('EMAIL_USER'),
                    [config('EMAIL_USER'), ],
                    # html_message=msg_html,
                )
                messages.success(
                    request, 'Your message has been sent succefully')
            except:
                messages.error(
                    request, 'Your message could not be sent! Check your internet and try again')
    else:
        form = ContactForm()

    context = {
        'form': form,
    }
    return render(request, "ace_the_essay/contact.html", context)
