from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models import fields
from .models import (
    Profile,
    ProjectOrder,
    Applicant,
    TestTask,
    Bid,
    CompleteTask,
)


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
            'deadline',
        ]
# Create bid form-(filled automatically when user clicks bid button on project detail view)


class BidForm(forms.ModelForm):

    class Meta:
        model = Bid
        fields = ['project', 'made_by']

# upload complete task form


class CompleteTaskForm(forms.ModelForm):

    class Meta:
        model = CompleteTask
        fields = ["complete_task"]

# Applicant writer form


class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = [
            'First_Name',
            'Last_Name',
            'Identification',
            'photo_id',
            'Highest_Level_of_Education',
            'CourseField_of_Study',
            'CV',
        ]

# Task form to upload test document on


class TaskForm(forms.ModelForm):
    class Meta:
        model = TestTask
        fields = ['test_task']
