from django import forms
from django.contrib.auth.forms import AuthenticationForm

class UserLoginForm(AuthenticationForm):
    pass

class RegistrationForm(AuthenticationForm):
    pass

class CodeSubmissionForm(forms.Form):
    LANGUAGE_CHOICES = [
        ('C++', 'C++'),
        ('Python', 'Python'),
        ('Java', 'Java'),
    ]
    language = forms.ChoiceField(choices=LANGUAGE_CHOICES)
    code = forms.CharField(widget=forms.Textarea)