from django.contrib import admin

# from django import forms
from .models import Applicant, Profile, ProjectOrder, Bid, CompleteTask, TestTask

admin.site.register(Profile)
admin.site.register(Applicant)
admin.site.register(ProjectOrder)
admin.site.register(Bid)
admin.site.register(CompleteTask)
admin.site.register(TestTask)
