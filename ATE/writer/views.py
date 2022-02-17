from datetime import timedelta
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Func
import json

from ace_the_essay.forms import LoginForm
from .forms import (
    EmailApplicationForm,
    ApplicantForm,
    TaskForm,
)
from users.forms import (
    ProfileUpdateForm,
    UserUpdateForm,
    ProfileUpdateForm,
    )
from client.models import ProjectOrder
from .models import Bid, Rating
from django.db.models.functions import TruncMonth, ExtractMonth
from django.db.models import (
    F, Q, Max, Min, Count, Aggregate
)
from django.contrib.auth import authenticate, login
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
    lform = LoginForm()
    msg = None

    if request.method == "POST":
        form = EmailApplicationForm(request.POST)
        lform = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')

            # Generate Password for the new applicant
            def password_Gen(length):

                # defined data to be used in the password
                lower = string.ascii_lowercase
                upper = string.ascii_uppercase
                num = string.digits
                # symbols = string.punctuation---------password too complicated for users

                # Combine the data
                all = lower + upper + num

                # use random to randomise the characters
                temp = random.sample(all, length)

                # create the password
                password_Gen.password = "".join(temp)
                return password_Gen.password

            # create account from email and password generated for the applicant
            try:
                user = User.objects.create_user(email,
                                                email,
                                                password_Gen(8))
                user.save()

                # add new applicant to Applicant user group

                def add_to_group(instance, created):
                    if created:
                        Applicants, created = Group.objects.get_or_create(name="Applicants")
                        instance.groups.add(Applicants)

                add_to_group(instance=user, created=isinstance)
                # # if django_user.groups.filter(name=groupname).exists():
                messages.success(request,
                                 "Your email has been submitted successfully")
                # Send credentials email to user
                try:
                    context = {
                        'username': email,
                        'password': password_Gen.password
                    }

                    msg_plain = render_to_string('mail/email.txt', context)
                #     # msg_html = render_to_string('templates/mail/email.html', context)

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
                messages.error(
                    request, "(X) There was a problem submitting your Email or Email already exists, try again after a few minutes!")
        elif lform.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("admin-landing")
            else:
                msg = "Wrong username or password given, please try again or click on 'forgot password'"
                messages.error(
                    request, "Login failed, click login again to see the problem")
    else:
        form = EmailApplicationForm()

    context = {
        'form': form,
        'loginform': lform,
        'msg': msg,
    }
    return render(request, "users/apply.html", context)

# applicant landing page view----------------------


@login_required
def application(request):
    usergroup = None
    usergroup = request.user.groups.values_list('name', flat=True).first()

    if usergroup == "Applicants" or usergroup == "Admin":
        current_user = request.user
        if request.method == "POST":
            form = ApplicantForm(request.POST,
                                 request.FILES)
            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.username = request.user
                new_form.save()
                messages.success(
                    request, "Your application has been sent successfully, please proceed with the TASK below!")

                try:
                    send_mail(
                        'NEW APPLICANT',
                        'New applicant registered',
                        config('EMAIL_USER'),
                        [config('EMAIL_USER'), ],
                        # html_message=msg_html,
                    )
                except:
                    pass
                return HttpResponseRedirect("application-task")
        else:
            form = ApplicantForm()

        context = {
            'Applicantform': form,
            'user': current_user,
        }
        return render(request, 'applicant/application.html', context)
    else:
        return HttpResponseBadRequest('You do not have permission to view this page! -The Team @ACE')


@login_required
def application_task(request):
    usergroup = None
    usergroup = request.user.groups.values_list('name', flat=True).first()

    if usergroup == "Applicants" or usergroup == "Admin":
        form = TaskForm(request.POST,
                        request.FILES)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.username = request.user
            new_form.save()
            applicant = request.user
            try:
                send_mail(
                    'TEST TASK',
                    f'Test task uploaded by {applicant}',
                    config('EMAIL_USER'),
                    [config('EMAIL_USER'), ],
                    # html_message=msg_html,
                )
            except:
                pass

            messages.success(
                request, "Task has been uploaded successfully! Please wait for feedback in the next 3-6 business days or sooner")
        else:
            form = TaskForm()
            messages.info(
                request, 'You can only upload a task once, please be thorough!')
        return render(request, 'applicant/application_task.html', {'form': form})
    else:
        return HttpResponseBadRequest('You do not have permission to view this page! -The Team @ACE')

# ------------------Writer dashboard views-----------------#

# usergroup check


def usergroup_check(user):
    usergroup = None
    usergroup = user.groups.values_list('name', flat=True).first()
    if usergroup == "Writers" or usergroup == "Admin":
        return True
    return False

    
# writer dashboard view


@login_required
@user_passes_test(usergroup_check, login_url=reverse_lazy('login'))
def writer(request):
    # count complete projects in the last month
    count_complete = ProjectOrder.objects.filter(bid__made_by=request.user,
                                                 bid__assign=True,
                                                 complete=True,
                                                 update_time__gt=F('date_posted') - timedelta(days=30)).count()

    def get_rank():  # fix this function
        count_complete = ProjectOrder.objects.filter(bid__made_by=request.user,
                                                     bid__assign=True,
                                                     complete=True,
                                                     update_time__gt=F('date_posted') - timedelta(days=30)).count()
        writers = ProjectOrder.objects.exclude(bid__in=ProjectOrder.bid_set.filter(
            bid__made_by=request.user,
            bid__assign=True,
            complete=True,
            update_time__gt=F('date_posted') - timedelta(days=30)
        )).count()
        return writers

    # rank = get_rank()
    active_projects = ProjectOrder.objects.filter(
        bid__made_by=request.user, bid__assign=True).order_by('-date_posted')[:2]
    recommended_project = ProjectOrder.objects.filter(
        bid__assign=False).order_by('-date_posted')[:1]
    complete_projects = ProjectOrder.objects.filter(bid__made_by=request.user,
                                                    bid__assign=True,
                                                    complete=True)[:2]

    projects_monthly = ProjectOrder.objects.annotate(month=ExtractMonth('date_posted')).values(
        'month').annotate(c=Count('id')).values('month', 'c').order_by()
    
    # convert the numeric date to string representation
    def get_month(month):
        if month == 1:
            return "January"
        elif month == 2:
            return "February"
        elif month == 3:
            return "March"
        elif month == 4:
            return "April"
        elif month == 5:
            return "May"
        elif month == 6:
            return "June"
        elif month == 7:
            return "July"
        elif month == 8:
            return "August"
        elif month == 9:
            return "September"
        elif month == 10:
            return "October"
        elif month == 11:
            return "November"
        elif month == 12:
            return "December"
    
    
    print("")
    print("")
    for data in projects_monthly:
        count = data['c']
        month = data['month']
        print(get_month(month))
        print(count)
    # print(projects_monthly)
    # print(projects_monthly)
    print("")
    print("")

    # user = request.user
    # rating = user.rating_set.all()
    # def get_score(rating):
    #     agg = 0
    #     count = 0
    #     for rating in rating:
    #         agg = agg + rating.score
    #         count +=1
    #     avg = agg/count
    #     return avg
    
    # score = get_score(rating)
    context = {
        'projects': active_projects,
        'rank': '1',
        'recommended': recommended_project,
        'completedProjects': complete_projects,
        'count': count_complete,
    }

    return render(request, 'writer/writer.html', context)

# ProjectOrders page views {--------}

# main view

# Display projects according to the tabs on the page


@login_required
@user_passes_test(usergroup_check, login_url=reverse_lazy('login'))
def projects(request):

    context = {
        'projects': ProjectOrder.objects.all(),
        'assigned': ProjectOrder.objects.filter(bid__assign=True, bid__made_by=request.user)
    }

    return render(request, 'writer/projects.html', context)

# search results view


@login_required
@user_passes_test(usergroup_check, login_url=reverse_lazy('login'))
def search_results(request):
    search_text = request.GET.get('q', '')
    results = ProjectOrder.objects.filter(title__icontains=search_text)
    return render(request, 'writer/results.html', {'results': results})

# writer bids view


@login_required
@user_passes_test(usergroup_check, login_url=reverse_lazy('login'))
def writer_bids(request):
    context = {
        'bids': Bid.objects.filter(made_by=request.user)
    }
    return render(request, "writer/writer_bids.html", context)
# Invoices view


@login_required
@user_passes_test(usergroup_check, login_url=reverse_lazy('login'))
def invoices(request):
    complete = ProjectOrder.objects.filter(
        complete=True,
        bid__made_by=request.user
    )
    assigned = ProjectOrder.objects.filter(
        bid__assign=True,
        bid__made_by=request.user
    )
    context = {
        'complete': complete,
        'assigned': assigned,
    }
    return render(request, 'writer/invoices.html', context)

# reports view


@login_required
@user_passes_test(usergroup_check, login_url=reverse_lazy('login'))
def reports(request):
    return render(request, 'writer/reports.html')

# settings view


@login_required
@user_passes_test(usergroup_check, login_url=reverse_lazy('login'))
def settings(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(
                request, f'Your account has been updated!')
            return redirect('settings')

    # **User is disabled with this function**

    # to make sure the user requesting disable is the owner
    elif request.GET.get('username') == request.user.username:
        username = request.user.username

        # function to disable a user
        def delete_user(request, username):
            context = None

            try:
                user = User.objects.get(username=username)
                user.is_active = False
                user.save()
                context = 'Profile successfully disabled. Thank you for using our service, cheers!'

            except User.DoesNotExist:
                context = 'User does not exist.'
            except Exception as e:
                context = e.message

           # send email to admin
            try:
                ctext = {
                    'username': username,
                }

                msg_plain = render_to_string('mail/email.txt', ctext)
                send_mail(
                    'ACCOUNT DISABLED',
                    msg_plain,
                    config('EMAIL_USER'),
                    [config('EMAIL_USER'), ],
                    # html_message=msg_html,
                )
            except:
                pass

            return context

        context = {
            'msg': delete_user(request, username),
        }

        return render(request, "users/user_delete.html", context)

    elif request.GET.get('username') != None and request.GET.get('username') != request.user.username:
        messages.error(request, "Username mismatch!")

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'writer/settings.html', context)


@login_required
@user_passes_test(usergroup_check, login_url=reverse_lazy('login'))
def library(request):
    messages.info(request, "Information will be made available soon.")
    return render(request, "writer/library.html")

# ------------------End Writer dashboard views-----------------#
