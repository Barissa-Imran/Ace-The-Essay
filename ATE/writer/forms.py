from django import forms
from .models import (
    Bid,
    CompleteTask,
    Applicant,
    TestTask,
    Rating
)



# Application page email form


class EmailApplicationForm(forms.Form):
    email = forms.EmailField(required=True)

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

# create a review form
class RatingForm(forms.ModelForm):

    class Meta:
        model = Rating
        fields = [
            'score',
            'review',
        ]