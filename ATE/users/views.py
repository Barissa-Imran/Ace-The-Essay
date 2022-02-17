from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from django.utils import timezone
from .forms import UserRegisterForm
from ace_the_essay.forms import LoginForm
from decouple import config


# Type of messages
"""
messages.debug
messages.info
messages.success
messages.warning
messages.error """

# register page view


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        lform = LoginForm(request.POST)
        msg = None

        if form.is_valid():
            user = form.save()
            # test case----
            Clients, created = Group.objects.get_or_create(name='Clients')
            user.groups.add(Clients)
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
        elif lform.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("admin_landing")
            else:
                msg = "Wrong username or password given, please try again or click on forgot password"
                messages.error(request, "Login failed, click login again to see the problem")

    else:
        form = UserRegisterForm()
        lform = LoginForm()
        msg = None

    context = {
        'userForm': form,
        'form': lform,
        'msg': msg,
    }
    return render(request, 'users/register.html', context)

# Admin landing page


@login_required
def admin_landing(request):
    # Redirect logged in users according to user group
    usergroup = None
    usergroup = request.user.groups.values_list('name', flat=True).first()
    if usergroup == "Admin":
        messages.info(
            request, "Check logs below to see what's new in version")
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



