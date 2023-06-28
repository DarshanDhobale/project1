from django import forms
from django.contrib.auth.forms import AuthenticationForm

class UserLoginForm(AuthenticationForm):
    pass

class RegistrationForm(AuthenticationForm):
    pass

class CodeSubmissionForm(forms.Form):
    code = forms.CharField(widget=forms.Textarea)