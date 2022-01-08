from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
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
    TaskForm,
    BidForm,
    CompleteTaskForm,
)
from .models import Bid, ProjectOrder
# Class based views
from django.views.generic import (
    DetailView,
    DeleteView,
    CreateView,
    UpdateView
)
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
        return HttpResponseBadRequest('You do not have permission to view this page! -Ate Team')


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

# Admin landing page


@login_required
def admin_landing(request):
    # Redirect logged in users according to user group
    usergroup = None
    usergroup = request.user.groups.values_list('name', flat=True).first()
    if usergroup == "Admin":
        messages.info(request, "Select a page you would like to visit below!")
        return render(request, "users/admin_landing.html")
    elif usergroup == "Writers" or usergroup == "Admin":
        return HttpResponseRedirect('writer')
    elif usergroup == "Applicants" or usergroup == "Admin":
        return HttpResponseRedirect('applicant/application')
    elif usergroup == "Clients" or usergroup == "Admin":
        # check if it's first client login then redirect to place order page.
        if User.last_login is None:
            return HttpResponseRedirect('client/place_order.html')
        else:
            return HttpResponseRedirect('client')
    else:
        messages.info(
            request, "you have been logged in but can't be redirected to the correct page, contact admin!!")
        return HttpResponseRedirect('login')


# ------------------Writer dashboard views-----------------#
# writer dashboard view

@login_required
def writer(request):

    def count_complete():
        count = 0
        completed = ProjectOrder.objects.filter(bid__made_by=request.user,
                                                bid__assign=True,
                                                complete=True)
        for project in completed:
            count += 1
        return count

    context = {
        'projects': ProjectOrder.objects.filter(bid__made_by=request.user, bid__assign=True)[:2],
        'recommended': ProjectOrder.objects.filter(bid__assign=False)[:1],
        'completedProjects': ProjectOrder.objects.filter(bid__made_by=request.user,
                                                         bid__assign=True,
                                                         complete=True)[:2],
        'count': count_complete(),
    }

    return render(request, 'writer/writer.html', context)

# ProjectOrders page views {--------}

# main view

# Display projects according to the tabs on the page


@login_required
def projects(request):

    context = {
        'projects': ProjectOrder.objects.all(),
        'assigned': ProjectOrder.objects.filter(bid__assign=True)
    }

    return render(request, 'writer/Projects.html', context)

# search results view


@login_required
def search_results(request):
    search_text = request.GET.get('q', '')
    results = ProjectOrder.objects.filter(title__icontains=search_text)
    return render(request, 'writer/results.html', {'results': results})

# writer bids view


@login_required
def writer_bids(request):
    context = {
        'bids': Bid.objects.filter(made_by=request.user)
    }
    return render(request, "writer/writer_bids.html", context)
# Invoices view


@login_required
def invoices(request):
    complete = ProjectOrder.objects.filter(
        complete=True, bid__made_by=request.user)
    assigned = ProjectOrder.objects.filter(
        bid__assign=True, bid__made_by=request.user)
    context = {
        'complete': complete,
        'assigned': assigned,
    }
    return render(request, 'writer/invoices.html', context)

# reports view


@login_required
def reports(request):
    return render(request, 'writer/reports.html')

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
                request, f'Your account has been updated!')
            return redirect('settings')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'writer/settings.html', context)

@login_required
def library(request):
    messages.info(request, "Information will be made available soon.")
    return render(request, "writer/library.html")

# ------------------End Writer dashboard views-----------------#


# ------------------Client dashboard views-----------------#

@login_required
def client(request):

    context = {
        'projects': ProjectOrder.objects.filter(username=request.user)
    }

    return render(request, 'client/client.html', context)


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

    # Get detail template according to user.
    def get_template_names(self):
        usergroup = None
        usergroup = self.request.user.groups.values_list(
            'name', flat=True).first()

        if usergroup == "Writers" or usergroup == "Admin":
            return ["writer/projectorder_detail.html"]
        elif usergroup == "Clients" or usergroup == "Admin":
            return ["client/projectorder_detail.html"]
        else:
            HttpResponseBadRequest("You are not allowed to access this page")

    # Get the forms ready to be produced them in the template (context)
    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        project = self.model.title
        context.update({
            'cForm': CompleteTaskForm,
            'bForm': BidForm,
            'project': project,
        })

        return context

    # Bid form validation
    def bForm_form_valid(self, request, form):
        form.instance.project = self.request.ProjectOrder
        form.instance.made_by = self.request.user
        messages.success(
            request, "Your bid has been submitted successfuly. View all bids by clicking on the Bids tab")
        return super().form_valid(form)

    # Complete task form validation
    def cForm_form_valid(self, request, form):
        form.instance.project = self.request.ProjectOrder
        project = self.request.ProjectOrder
        form.instance.bid = project.bid.filter(made_by=self.request.user)
        messages.success(request, "Project was submitted successfully")
        return super().form_valid(form)


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = ProjectOrder
    template_name = "client/projectorder_form.html"
    fields = [
        'academic_level',
        'type_of_paper',
        'subject_area',
        'title',
        'paper_instructions',
        'Additional_materials',
        'paper_format',
        'number_of_pages',
        'spacing',
        'currency',
        'date_posted',
    ]

    def form_valid(self, form):
        form.instance.slug = str(form.instance.title) + \
            '-' + str(form.instance.pk)
        form.instance.username = self.request.user
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = ProjectOrder
    fields = [
        'academic_level',
        'type_of_paper',
        'subject_area',
        'title',
        'paper_instructions',
        'Additional_materials',
        'paper_format',
        'number_of_pages',
        'spacing',
        'currency',
        'date_posted',
    ]


@login_required
def client_projects(request):
    context = {
        'projects': ProjectOrder.objects.filter(username=request.user)
    }
    return render(request, 'client/client_projects.html', context)


@login_required
def client_bids(request):
    context = {
        'bids': Bid.objects.filter(project__username=request.user)
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

# ------------------------End client dahsboard views--------------------------#
