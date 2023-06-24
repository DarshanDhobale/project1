from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Userprofile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)

class Problem(models.Model):
    title = models.CharField(max_length=255)
    statement = models.TextField()

class Submission(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    input_data = models.TextField()
    expected_output = models.TextField()

class Result(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    error_message = models.TextField(blank=True, null=True)