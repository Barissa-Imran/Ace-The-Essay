from django import forms
from .models import Contact
# Contact us form


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)
