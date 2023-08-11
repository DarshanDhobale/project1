from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Userprofile,Problem,Submission,TestCase
# Register your models here.

admin.site.register(Userprofile)
admin.site.register(Problem)
admin.site.register(Submission)
admin.site.register(TestCase)
