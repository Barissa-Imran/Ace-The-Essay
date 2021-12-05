from django.contrib import admin

from django import forms
from .models import Applicant, Profile, ProjectOrder

# custom project order form with price field editable


class CustomProjectOrderForm(forms.ModelForm):
    price = forms.FloatField()

    class Meta:
        model = ProjectOrder
        fields = '__all__'


class ProjectOrderAdmin(admin.ModelAdmin):
    form = CustomProjectOrderForm


admin.site.register(Profile)
admin.site.register(Applicant)
admin.site.register(ProjectOrder, ProjectOrderAdmin)
