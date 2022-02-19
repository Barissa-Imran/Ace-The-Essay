from datetime import timedelta
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http.response import HttpResponseBadRequest
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
from users.forms import (
    UserUpdateForm,
    ProfileUpdateForm,
)
from writer.forms import BidForm, CompleteTaskForm, RatingForm
from .models import ProjectOrder
from writer.models import Bid, Rating
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
from django.db.models.functions import ExtractMonth, Extract
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
    # count project orders made in a span of a month
    count = ProjectOrder.objects.filter(username=request.user, update_time__gt=F(
        'date_posted') - timedelta(days=30)).count()
    # count all project orders made by the user
    total_count = ProjectOrder.objects.filter(username=request.user).count()
    # get the latest projects from the user
    featured_projects = ProjectOrder.objects.filter(
        username=request.user).order_by('-date_posted')[:2]
    # get lates invoices made to the user
    invoices = ProjectOrder.objects.filter(
        bid__assign=True, username=request.user)[:2]
    # Group project orders by month
    projects_monthly = ProjectOrder.objects.annotate(month=ExtractMonth('date_posted')).values(
        'month').annotate(c=Count('id', filter=Q(username=request.user))).values('month', 'c').order_by()

    projects_writer = ProjectOrder.objects.values('bid__made_by').annotate(
        c=Count('id', filter=Q(bid__assign=True))).order_by()

    print("")
    print("")

    # get the data
    c = []
    for i in projects_writer:
        c.append(i['c'])

    high = max(c)
    writer = None
    writer_count = 0
    for i in projects_writer:
        if i['c'] == high:
            userId = i['bid__made_by']
            if userId is not None:
                user = User.objects.get(id=userId)
                writer = user
                writer_count = i['c']
            else:
                pass
        pass
    
    print("")
    print("")

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

    # this section is used in getting chat data
    data = []
    labels = []
    for i in projects_monthly:
        counter = i['c']
        month = i['month']

        data.append(counter)
        labels.append(get_month(month))

    # print(data)

    context = {
        'writer': writer,
        'writer_count': writer_count,
        'projects': featured_projects,
        'invoices': invoices,
        'recommended': '',
        'count': count,
        'total_count': total_count,
        'labels': json.dumps(labels),
        'data': json.dumps(data),
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

    # provide custom context i for the view i.e forms
    def get_context_i(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_i(**kwargs)
        project = self.get_object()
        user = self.request.user
        client_bids = Bid.objects.filter(project__id=project.id)
        client_bids_assign = Bid.objects.filter(
            project__id=project.id, assign=True)

        def get_rating():
            for bid in client_bids_assign:
                user = bid.made_by
                rating = user.rating_set.all()

                agg = 0
                count = 0
                for rating in rating:
                    agg = agg + rating.score
                    count += 1
                    avg = agg/count
                return avg

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
            'rate': get_rating()
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
            form = RatingForm(request.POST)
            if request.POST.get('form') == "mark-complete":
                project = self.get_object()
                if project.complete is False:
                    try:
                        project.complete = True
                        project.save()

                        # {send notification to client/admin}

                        # no request hence no message
                        messages.success(
                            request, "Order completed successfully.")
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
            elif request.POST.get('form') == "review-form":
                project = self.get_object()
                client_bids_assign = Bid.objects.filter(
                    project__id=project.id, assign=True)

                def get_reviewee(client_bids_assign):
                    for bid in client_bids_assign:
                        return bid.made_by

                score = request.POST.get('rating')
                review = request.POST.get('review')
                username = get_reviewee(client_bids_assign)
                reviewed_by = self.request.user

                Rating.objects.create(
                    username=username,
                    score=score,
                    review=review,
                    reviewed_by=reviewed_by,
                )

                # form.instance.username = username
                # form.instance.score = score
                # form.instance.review = review
                # form.instance.reviewed_by = self.request.user
                # form.save()
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

        # get context i for post request redirect-------------------
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

    # validate the form and add i to empty fields as specified
    def form_valid(self, form):

        # generate random unique characters to be used in the slug
        def char_Gen(length):

            # defined i to be used in the characters
            lower = string.ascii_lowercase
            upper = string.ascii_uppercase
            num = string.digits

            # Combine the i
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

            # defined i to be used in the characters
            lower = string.ascii_lowercase
            upper = string.ascii_uppercase
            num = string.digits

            # Combine the i
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
                request, f'Your account has been updated!')
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
