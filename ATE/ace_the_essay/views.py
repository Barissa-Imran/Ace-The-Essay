from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail
from decouple import config
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from django.shortcuts import HttpResponseRedirect
from django.views.generic import TemplateView
from .forms import ContactForm, LoginForm


class indexView(TemplateView):
    template_name = 'ace_the_essay/core.html'

    # log user in from the popup
    def post(self, request):
        form = LoginForm(request.POST)
        msg = None
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("auth/admin-landing")
            else:
                msg = "Wrong username or password given, please try again or click on 'forgot password'"
                messages.error(
                    request, "Login failed, click login again to see the problem")
        else:
            pass

        content = {'form': form, 'msg': msg}
        return render(request, "ace_the_essay/core.html", content)


class whyusView(TemplateView):
    template_name = 'ace_the_essay/whyus.html'

    # log user in from the popup
    def post(self, request):
        form = LoginForm(request.POST)
        msg = None
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("auth/admin-landing")
            else:
                msg = "Wrong username or password given, please try again or click on 'forgot password'"
                messages.error(
                    request, "Login failed, click login again to see the problem")
        else:
            pass

        content = {'form': form, 'msg': msg}
        return render(request, "ace_the_essay/whyus.html", content)


class topView(TemplateView):
    template_name = "ace_the_essay/top.html"

    def post(self, request):
        form = LoginForm(request.POST)
        msg = None
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("auth/admin-landing")
            else:
                msg = "Wrong username or password given, please try again or click on 'forgot password'"
                messages.error(
                    request, "Login failed, click login again to see the problem")
        else:
            pass

        content = {'form': form, 'msg': msg}
        return render(request, "ace_the_essay/top.html", content)


class faqView(TemplateView):
    template_name = "ace_the_essay/faq.html"

    def post(self, request):
        form = LoginForm(request.POST)
        msg = None
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("auth/admin-landing")
            else:
                msg = "Wrong username or password given, please try again or click on 'forgot password'"
                messages.error(
                    request, "Login failed, click login again to see the problem")
        else:
            pass

        content = {'form': form, 'msg': msg}
        return render(request, "ace_the_essay/faq.html", content)


class revisionPolicyView(TemplateView):
    template_name = "ace_the_essay/revision-policy.html"

    def post(self, request):
        form = LoginForm(request.POST)
        msg = None
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("auth/admin-landing")
            else:
                msg = "Wrong username or password given, please try again or click on 'forgot password'"
                messages.error(
                    request, "Login failed, click login again to see the problem")
        else:
            pass

        content = {'form': form, 'msg': msg}
        return render(request, "ace_the_essay/revision-policy.html", content)


class privacyPolicyView(TemplateView):
    template_name = "ace_the_essay/privacy-policy.html"

    def post(self, request):
        form = LoginForm(request.POST)
        msg = None
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("auth/admin-landing")
            else:
                msg = "Wrong username or password given, please try again or click on 'forgot password'"
                messages.error(
                    request, "Login failed, click login again to see the problem")
        else:
            pass

        content = {'form': form, 'msg': msg}
        return render(request, "ace_the_essay/privacy-policy.html", content)


class termsView(TemplateView):
    template_name = "ace_the_essay/TC.html"

    def post(self, request):
        form = LoginForm(request.POST)
        msg = None
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("auth/admin-landing")
            else:
                msg = "Wrong username or password given, please try again or click on 'forgot password'"
                messages.error(
                    request, "Login failed, click login again to see the problem")
        else:
            pass

        content = {'form': form, 'msg': msg}
        return render(request, "ace_the_essay/TC.html", content)


class HIWView(TemplateView):
    template_name = "ace_the_essay/hiw.html"

    def post(self, request):
        form = LoginForm(request.POST)
        msg = None
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("auth/admin-landing")
            else:
                msg = "Wrong username or password given, please try again or click on 'forgot password'"
                messages.error(
                    request, "Login failed, click login again to see the problem")
        else:
            pass

        content = {'form': form, 'msg': msg}
        return render(request, "ace_the_essay/hiw.html", content)

# contact page view


class contactView(TemplateView):
    template_name = "ace_the_essay/contact.html"

    # contact form config
    def form_valid(self, form):
        name = form.instance.name
        email = form.instance.email
        subject = form.instance.subject
        message = form.instance.message

        try:
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
                self.request, 'Your message has been sent succefully')

        except:
            pass

        return super().form_valid(form)

    # post request method
    def post(self, request):
        # Login form config
        form = LoginForm(request.POST)
        msg = None
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("auth/admin-landing")
            else:
                msg = "Wrong username or password given, please try again or click on 'forgot password'"
                messages.error(
                    request, "Login failed, click login again to see the problem")
        else:
            pass

        # contact form config
        def contact(request):
            cform = ContactForm(request.POST)
            if cform.is_valid():

                # only save the message if the email is sent to admin
                try:
                    cform.save()

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

            return cform

        content = {'form': form, 'cform': contact(request), 'msg': msg}
        return render(request, "ace_the_essay/contact.html", content)