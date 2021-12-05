from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, ProjectOrder, Applicant

# Company registration page registration form


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Profile page user update forms----------------


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
# ---------------------------------------------

# Application page email form


class EmailApplicationForm(forms.Form):
    email = forms.EmailField(required=True)

# client Project order form----------------
# view admin.py for admin form
class ProjectOrderForm(forms.ModelForm):
    class Meta:
        model = ProjectOrder
        fields = '__all__'

# Applicant writer form
class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = '__all__'

# Task form to upload test document on
class TaskForm(forms.Form):
    test_task = forms.FileField(help_text='Upload the completed test task here')