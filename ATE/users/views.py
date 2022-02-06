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

from ace_the_essay.forms import LoginForm
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
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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
        messages.info(
            request, "Website is now fully mobile responsive. Open on mobile to experience (~_~)")
        return render(request, "users/admin_landing.html")
    elif usergroup == "Writers" or usergroup == "Admin":
        return HttpResponseRedirect('writer')
    elif usergroup == "Applicants" or usergroup == "Admin":
        return HttpResponseRedirect('applicant/application')
    elif usergroup == "Clients" or usergroup == "Admin":
        # check if it's first client login then redirect to place order page.
        user = request.user
        if user.last_login == timezone.now():  # fix this
            return HttpResponseRedirect('client/placeorder_form.html')
        else:
            return HttpResponseRedirect('client')
    else:
        messages.info(
            request, "you have been logged in but can't be redirected to the correct page, contact admin!!")
        return HttpResponseRedirect('login')


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


# ------------------Client dashboard views-----------------#

# usergroup check
def usergroup_check(user):
    usergroup = None
    usergroup = user.groups.values_list('name', flat=True).first()
    if usergroup == "Clients" or usergroup == "Admin":
        return True
    return False


@login_required
@user_passes_test(usergroup_check, login_url=reverse_lazy('login'))
def client(request):
    count = ProjectOrder.objects.filter(username=request.user, update_time__gt=F(
        'date_posted') - timedelta(days=30)).count()
    featured_projects = ProjectOrder.objects.filter(
        username=request.user).order_by('-date_posted')[:2]
    invoices = ProjectOrder.objects.filter(bid__assign=True, username=request.user)[:2]

    context = {
        'projects': featured_projects,
        'invoices': invoices,
        'recommended': '',
        'count': count,
    }

    return render(request, 'client/client.html', context)

class ProjectDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = ProjectOrder

    def test_func(self):
        usergroup = None
        usergroup = self.request.user.groups.values_list(
            'name', flat=True).first()
        if usergroup == "Writers" or usergroup == "Admin" or usergroup == "Clients":
            return True
        return False

    # Get detail template according to user.
    def get_template_names(self):
        usergroup = None
        usergroup = self.request.user.groups.values_list(
            'name', flat=True).first()
        if usergroup == "Writers":
            return ["writer/projectorder_detail.html"]
        elif usergroup == "Clients" or usergroup == "Admin":
            return ["client/projectorder_detail.html"]
        else:
            return HttpResponseBadRequest("You are not allowed to access this page")

    # provide custom context data for the view i.e forms
    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        project = self.get_object()
        user = self.request.user
        client_bids = Bid.objects.filter(project__id=project.id)
        client_bids_assign = Bid.objects.filter(
            project__id=project.id, assign=True)

        # to get the complete uploaded document for the order
        def get_file():
            bids = project.bid_set.all()
            for bid in bids:
                files = bid.completetask_set.all()
                for file in files:
                    return file  # fix to show file instead of url

        uploaded_project = get_file()

        # only show complete task section if user is assigned order

        def func(project, user):
            bids = project.bid_set.all()
            if bids.exists():
                for bid in bids:
                    if bid.made_by == user and bid.assign == True:
                        return True
                    pass
            else:
                return False

        # only show bid button if order is not assigned yet
        def func2(project):
            bids = project.bid_set.all()
            if bids.exists():
                for bid in bids:
                    if bid.assign == False or bid == None:
                        return False
                    pass
            else:
                return False
        # Check to see if user has submitted a bid on the project prevent multiple

        def func3(project, user):
            bids = project.bid_set.all()
            if bids.exists():
                for bid in bids:
                    if bid.made_by == user:
                        return True
                    pass
            else:
                return False

        # get the current user's usergroup
        usergroup = None
        usergroup = self.request.user.groups.values_list(
            'name', flat=True).first()

        # to pass admin user into the context as True
        def get_admin(usergroup):
            Admin = None
            if usergroup == "Admin":
                return True
            return False

        context.update({
            'cForm': CompleteTaskForm,
            'bForm': BidForm,
            'client_bids': client_bids,
            'client_bids_assign': client_bids_assign,
            'assigned': func(project, user),
            'bid': func2(project),
            'usergroup': get_admin(usergroup),
            'bid_sent': func3(project, user),
            'uploaded_project': uploaded_project,
        })

        return context

    # Post request handler (Complete task & Bid form)
    def post(self, request, *args, **kwargs):
        bform = BidForm(request.POST)
        cform = CompleteTaskForm(request.POST,
                                 request.FILES)

        # bidForm section
        if bform.is_valid():
            project = self.get_object()
            bids = project.bid_set.all()

            if bids.exists():
                for bid in bids:
                    if bid.made_by == request.user:
                        bid.delete()
                        messages.info(request, "Bid reverted successfully")
                    else:
                        try:
                            new_bform = bform.save(commit=False)
                            new_bform.project = self.get_object()
                            new_bform.made_by = self.request.user
                            new_bform.save()

                            messages.success(
                                request, "Your bid has been submitted successfully")
                        except:
                            messages.error(
                                request, "Bid sending error, Try again later")
            else:
                try:
                    new_bform = bform.save(commit=False)
                    new_bform.project = self.get_object()
                    new_bform.made_by = self.request.user
                    new_bform.save()

                    messages.success(
                        request, "Your bid has been submitted successfully")
                except:
                    messages.error(
                        request, "Bid sending error, Try again later")

        # completeTaskForm section
        elif cform.is_valid():
            try:
                project = self.get_object()
                new_cform = cform.save(commit=False)
                new_cform.project = self.get_object()

                # get bid for current project
                def bid(project, request):
                    bids = project.bid_set.all()
                    for bid in bids:
                        if bid.made_by == request.user:
                            return bid
                        else:
                            pass

                new_cform.bid = bid(project, request)
                new_cform.save()

                # {send notification and email to client/admin}

                messages.success(
                    request, "File uploaded successfully, please wait for feedback")
            except:
                messages.error(
                    request, "File upload failed. Please try again later")

        # handle mark as complete post request from client detail page
        elif request.is_ajax():
            project = self.get_object()
            if project.complete is False:
                try:
                    project.complete = True
                    project.save()

                    # {send notification to client/admin}

                    # no request hence no message
                    messages.success(request, "Order completed successfully.")
                except:
                    messages.error(
                        request, "request failed, please try again later")
            elif project.complete is True:
                try:
                    project.complete = False
                    project.save()
                    messages.info(request, "Action reverted successfully")
                except:
                    messages.error(
                        request, "request failed, please try again later")

        # handle writter assignment to projects
        else:
            try:
                id = request.POST.get('bidId')
                bid = Bid.objects.get(id=id)

                if bid.assign == False:
                    try:
                        bid.assign = True
                        bid.save()
                        messages.success(
                            request, "Writer assigned successfully")
                    except:
                        messages.error(
                            request, "writer assignment failed, please try again!")
                else:
                    bid.assign = False
                    bid.save()
                    messages.info(request, "Assignment reverted successfully")
            except:
                pass

        # get context data for post request redirect-------------------
        # to get the complete uploaded document for the order

        def get_file(project):
            bids = project.bid_set.all()
            for bid in bids:
                files = bid.completetask_set.all()
                for file in files:
                    return file  # fix to show file instead of url

        # only show complete task section is user is assigned order

        def func(project, user):
            bids = project.bid_set.all()
            for bid in bids:
                if bid.made_by == user and bid.assign == True:
                    return True
                pass

        # only show bid button if order is not assigned yet
        def func2(project):
            bids = project.bid_set.all()
            if bids.exists():
                for bid in bids:
                    if bid.assign == False or bid == None:
                        return False
                    pass
            else:
                return False

        # Check to see if user has submitted a bid on the project prevent multiple
        def func3(project, user):
            bids = project.bid_set.all()
            if bids.exists():
                for bid in bids:
                    if bid.made_by == user:
                        return True
                    pass
            else:
                return False

        # get the current user's usergroup
        usergroup = None
        usergroup = self.request.user.groups.values_list(
            'name', flat=True).first()

        # to pass admin user into the context as True
        def get_admin(usergroup):
            Admin = None
            if usergroup == "Admin":
                return True
            return False

        project = self.get_object()
        user = self.request.user
        uploaded_project = get_file(project)
        client_bids = Bid.objects.filter(project__id=project.id)
        client_bids_assign = Bid.objects.filter(
            project__id=project.id, assign=True)

        context = {
            'form': bform,
            'cForm': cform,
            'bForm': bform,
            'client_bids': client_bids,
            'client_bids_assign': client_bids_assign,
            'bid_sent': func3(project, user),
            'assigned': func(project, user),
            'bid': func2(project),
            'usergroup': get_admin(usergroup),
            'object': self.get_object(),
            'uploaded_project': uploaded_project,
        }
        # check usergroup to return appropriate page client/writer
        if usergroup == "Writers":
            return render(request, "writer/projectorder_detail.html", context)
        else:
            return render(request, "client/projectorder_detail.html", context)


class ProjectCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
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
        'price',
        'deadline'
    ]

    def test_func(self):
        usergroup = None
        usergroup = self.request.user.groups.values_list(
            'name', flat=True).first()
        if usergroup == "Admin" or usergroup == "Clients":
            return True
        return False

    #validate the form and add data to empty fields as specified
    def form_valid(self, form):

        # generate random unique characters to be used in the slug
        def char_Gen(length):

            # defined data to be used in the characters
            lower = string.ascii_lowercase
            upper = string.ascii_uppercase
            num = string.digits

            # Combine the data
            all = lower + upper + num

            # use random to randomise the characters
            temp = random.sample(all, length)

            # create the char hash
            char = "".join(temp)
            return char
        
        try:
            # replace spaces in title with hiphens
            title = form.instance.title.replace(" ", "-")

            form.instance.slug = str(title) + \
                '-' + str(char_Gen(8))
            form.instance.username = self.request.user
            # return JsonResponse({'slug':form.instance.slug}, status=200)
        except:
            pass
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
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
        'price',
        'deadline'
    ]

    def form_valid(self, form):

        # generate random unique characters to be used in the slug
        def char_Gen(length):

            # defined data to be used in the characters
            lower = string.ascii_lowercase
            upper = string.ascii_uppercase
            num = string.digits

            # Combine the data
            all = lower + upper + num

            # use random to randomise the characters
            temp = random.sample(all, length)

            # create the char hash
            char = "".join(temp)
            return char

        # replace spaces in title with hiphens
        title = form.instance.title.replace(" ", "-")

        form.instance.slug = str(title) + \
            '-' + str(char_Gen(8))
        form.instance.username = self.request.user
        return super().form_valid(form)

    def test_func(self):
        project = self.get_object()
        if self.request.user == project.username:
            return True
        return False


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ProjectOrder
    template_name = "client/projectorder_confirm_delete.html"
    success_url = "/auth/order/deleted"

    def test_func(self):
        project = self.get_object()
        if self.request.user == project.username:
            return True
        return False


def project_deleted(request):
    return render(request, "client/projectorder_deleted.html")

@login_required
@user_passes_test(usergroup_check, login_url=reverse_lazy('login'))
def client_projects(request):
    context = {
        'projects': ProjectOrder.objects.filter(username=request.user)
    }
    return render(request, 'client/client_projects.html', context)


@login_required
@user_passes_test(usergroup_check, login_url=reverse_lazy('login'))
def client_bids(request):

    context = {
        'bids': Bid.objects.filter(project__username=request.user)
    }
    return render(request, "client/client_bids.html", context)


@login_required
@user_passes_test(usergroup_check, login_url=reverse_lazy('login'))
def client_invoices(request):
    complete = ProjectOrder.objects.filter(
        username=request.user,
        complete=True
    )
    assigned = ProjectOrder.objects.filter(
        username=request.user,
        bid__assign=True,
    )
    context = {
        'complete': complete,
        'assigned': assigned,
    }
    return render(request, 'client/client_invoices.html', context)


@login_required
@user_passes_test(usergroup_check, login_url=reverse_lazy('login'))
def client_reports(request):
    return render(request, 'client/client_reports.html')


@login_required
@user_passes_test(usergroup_check, login_url=reverse_lazy('login'))
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

    return render(request, 'client/client_settings.html', context)


@login_required
@user_passes_test(usergroup_check, login_url=reverse_lazy('login'))
def client_ProjectOrders(request):
    return render(request, 'client/client_ProjectOrders.html')

# ------------------------End client dashboard views--------------------------#
