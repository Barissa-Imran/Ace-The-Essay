from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import User, Group

from .forms import (
    EmailApplicationForm,
    UserRegisterForm,
    UserUpdateForm,
    ProfileUpdateForm,
    ProjectOrderForm,
    ApplicantForm,
    TaskForm
)
from .models import Bid, ProjectOrder
# Class based views
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
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

            # Generate Password for the new applicant
            def password_Gen(length):

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
                        instance.groups.add(
                            Group.objects.get(name="Applicants"))

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
    else:
        form = EmailApplicationForm()
    return render(request, "users/apply.html", {'form': form})

# applicant landing page view----------------------


@login_required
def application(request):
    usergroup = None
    usergroup = request.user.groups.values_list('name', flat=True).first()

    if usergroup == "Applicant" or usergroup == "Admin":
        user1 = request.user
        if request.method == "POST":
            form = ApplicantForm(request.POST,
                                 request.FILES)
            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.username = request.user
                new_form.save()
                messages.success(
                    request, 'Your application has been sent successfully! Please proceed to the TASK page')
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
        else:
            form = ApplicantForm()

        context = {
            'Applicantform': form,
            'user': user1,
        }
        return render(request, 'applicant/application.html', context)
    else:
        return HttpResponseBadRequest('You do not have permission to view this page! -Ate Team')


@login_required
def application_task(request):
    usergroup = None
    usergroup = request.user.groups.values_list('name', flat=True).first()

    if usergroup == "Applicant" or usergroup == "Admin":
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
        return HttpResponseBadRequest('You do not have permission to view this page')
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
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            try:
                send_mail(
                    'NEW CLIENT',
                    f'You have a new client registered. Username: {username} email: {email}',
                    config('EMAIL_USER'),
                    [config('EMAIL_USER'), ],
                    # html_message=msg_html,
                )
            except:
                pass
            messages.success(
                request, "Your account has been created! you are now able to log in")
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


# ------------------Writer dashboard views-----------------#
# writer dashboard view


@login_required
def writer(request):
    context = {
        'projects': ProjectOrder.objects.all()
    }
    # redirect the user according to user group
    usergroup = None
    usergroup = request.user.groups.values_list('name', flat=True).first()
    if usergroup == "Writers" or usergroup == "Admin":
        return render(request, 'users/writer.html', context)
    elif usergroup == "Applicants" or usergroup == "Admin":
        return HttpResponseRedirect('applicant/application')
    elif usergroup == "Clients" or usergroup == "Admin":
        # check to see if it's first login then redirect to order page
        return HttpResponseRedirect('client/client')
    else:
        messages.info(
            request, "you have been logged in but can't be redirected to the correct page, contact admin!!")
        return HttpResponseRedirect('login')

# ProjectOrders page views {--------}

# main view

# Display projects writer is working on


@login_required
def projects(request):

    context = {
        'projects': ProjectOrder.objects.all()
    }

    return render(request, 'users/Projects.html', context)

# Displays all projects created and active


@login_required
def all_projects(request):
    context = {
        'ProjectOrders': ProjectOrder.objects.all()
    }
    return render(request, 'users/allprojects.html')
# search results view


@login_required
def search_results(request):
    search_text = request.GET.get('q', '')
    results = ProjectOrder.objects.filter(title__icontains=search_text)
    return render(request, 'users/results.html', {'results': results})

# writer bids view


@login_required
def writer_bids(request):
    context = {
        'bids': Bid.objects.filter(made_by=request.user)
    }
    return render(request, "users/writer_bids.html", context)
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
            return redirect('client_settings')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/settings.html', context)

# ------------------End Writer dashboard views-----------------#


# ------------------Client dashboard views-----------------#

@login_required
def client(request):
    return render(request, 'client/client.html')


@login_required
def place_order(request):
    if request.method == 'POST':
        form = ProjectOrderForm(request.POST)

        if form.is_valid():
            new_form = form.save()
            title = new_form.title
            pk = new_form.pk
            # fix this functionality to produce raw string
            new_form.slug = str(title) + "-" + str(pk)
            new_form.username = request.user
            new_form.save()
            username = request.user

            # test case
            # made_by = request.user
            # bid = Bid.objects.create(project=new_form, made_by=made_by)
            # bid.save()

            try:
                send_mail(
                    'NEW ORDER',
                    f'There is a new order placed by {username} title: {title}',
                    config('EMAIL_USER'),
                    [config('EMAIL_USER'), ],
                    # html_message=msg_html,
                )
            except:
                pass
            messages.success(
                request, 'Your order has been placed successfully, Please wait to be contacted by admin about pricing')
    else:
        form = ProjectOrderForm()

    context = {
        'place_order': form,
    }
    return render(request, 'client/place_order.html', context)


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = ProjectOrder
    # request.session['click'] = True

    '''
    def get_context_data(self):
        context = super(ProjectDetailView, self).get_context_data()
        # Object is accessible through self.object or self.get_object()
        if request.session.pop('click', False):
            project = self.object
            made_by = request.user
            bid = Bid.objects.create(project=project, made_by=made_by)
            bid.save()
    '''

    def create_bid(self, request):

        if request.method == "POST":
            try:
                project = self.instance
                made_by = request.user
                bid = Bid.objects.create(project=project, made_by=made_by)
                bid.save()

                messages.success(
                    request, "Bid sent sucessfully! Wait for feedback from the project owner on the Bids Tab")
            except:
                messages.error(
                    request, 'cannot send multiple bids for one project')

        return render(request, 'users/projectorder_detail.html')


@login_required
def client_projects(request):
    return render(request, 'client/client_projects.html')


@login_required
def client_bids(request):
    context = {
        # 'bids': Bids.objects.all()
    }
    return render(request, "client/client_bids.html", context)


@login_required
def client_invoices(request):
    return render(request, 'client/client_invoices.html')


@login_required
def client_reports(request):
    return render(request, 'client/client_reports.html')


@login_required
def client_settings(request):
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
            return redirect('client_settings')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'client/client_settings.html', context)


@login_required
def client_ProjectOrders(request):
    return render(request, 'client/client_ProjectOrders.html')
