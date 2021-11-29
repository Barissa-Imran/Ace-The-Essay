from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, Group
from .forms import EmailApplicationForm, UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from decouple import config
# To be used in password creation
import random
import string


# Type of messages
"""
messages.debug
messages.info
messages.success
messages.warning
messages.error """

# ------------------Applicant views-----------------#
# apply page view


def apply(request):
    if request.method == "POST":
        form = EmailApplicationForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')

            # Generate Password for the new applicant (couldn't access the password outside function after return)
            # length of the password
            length = int(8)

            # defined data to be used in the password
            lower = string.ascii_lowercase
            upper = string.ascii_uppercase
            num = string.digits
            symbols = string.punctuation

            # Combine the data
            all = lower + upper + num + symbols

            # use random to randomise the characters
            temp = random.sample(all, length)

            # create the password
            password = "".join(temp)

            # create account from email and password generated for the applicant
            try:
                user = User.objects.create_user(email,
                                                email,
                                                password)
                user.save()

                # add new applicant to Applicant user group

                def add_to_group(instance, created):
                    if created:
                        instance.groups.add(
                            Group.objects.get(name="Applicants"))
                add_to_group(instance=user, created=isinstance)
                # if django_user.groups.filter(name=groupname).exists():
                messages.success(request,
                                 "Your email has been submitted successfully")
                # Send credentials email to user
                try:
                    context = {
                        'username': email,
                        'password': password
                    }
                    msg_plain = render_to_string('mail/email.txt', context)
                    # msg_html = render_to_string('templates/mail/email.html', context)

                    send_mail(
                        'LOGIN CREDENTIALS',
                        msg_plain,
                        config('EMAIL_USER'),
                        [email, ],
                        # html_message=msg_html,
                    )
                except:
                    messages.error(
                        request, 'Could not send email, click login above then forgot password!')
            except:
                messages.error(request, "(X) Email already exists, try again!")
    else:
        form = EmailApplicationForm()
    return render(request, "users/apply.html", {'form': form})

# applicant landing page view----------------------


@login_required
def application(request):
    return render(request, 'users/application.html')

# register page view


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # test case----
            group = Group.objects.get(name="Clients")
            user.groups.add(group)
            # end------test case
            messages.success(
                request, "Your account has been created! you are now able to log in")
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

# Profile page view- only accessible after login


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(
                request, f'Your account has been update!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)

# ------------------Writer dashboard views-----------------#
# writer dashboard view


@login_required
def writer(request):
    # redirect the user according to user group
    usergroup = None
    usergroup = request.user.groups.values_list('name', flat=True).first()
    if usergroup == "Writers":
        return HttpResponseRedirect('writer')
    elif usergroup == "Applicants":
        return HttpResponseRedirect('application')
    elif usergroup == "Clients":
        return HttpResponseRedirect('client')
    else:
        return HttpResponseRedirect('login')

# Projects page views {--------}


@login_required
def projects(request):
    return render(request, 'users/projects.html')

# Invoices view


@login_required
def invoices(request):
    return render(request, 'users/invoices.html')

# reports view


@login_required
def reports(request):
    return render(request, 'users/reports.html')

# settings view


@login_required
def settings(request):
    return render(request, 'users/settings.html')

# ------------------End Writer dashboard views-----------------#


# ------------------Client dashboard views-----------------#


@login_required
def client(request):
    return render(request, 'users/client.html')
