from django.db import models
from datetime import datetime
from django.db.models.signals import post_save
from django.contrib.auth.models import User
# Create your models here.

class Userprofile(models.Model):#models is a module provided by Django that contains various classes and utilities for defining and working with database models.class userprofile extends Class Model
    user= models.OneToOneField(User, on_delete=models.CASCADE)#
    total_solved= models.IntegerField(default=0)
    total_score= models.IntegerField(default=0)
    
    def __str__(self):
        return self.user.username
    

class Problem(models.Model):
    DIFFICULTY_CHOICES = [('Easy', 'Easy'),('Medium', 'Medium'),('Hard', 'Hard'),] #(value ,human readable) value is used when querying
    title = models.CharField(max_length=255)
    statement = models.TextField()
    time_limit = models.IntegerField(default=2, help_text="in seconds")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES ,null=True)#null = True denotes we can hsve no value or null 

    def __str__(self):#return string representation of object
        return self.title

class Submission(models.Model):
    LANGUAGE_CHOICES = [('C++', 'C++'),('Python', 'Python'),('Java', 'Java'),]
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)#foreignkey one problem to many submissions
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.TextField()
    language = models.CharField(max_length=10, choices= LANGUAGE_CHOICES)
    submitted_at = models.DateTimeField()
    user_stdout = models.TextField(max_length=10000, default="")
    user_stderr = models.TextField(max_length=10000, default="")
    run_time = models.FloatField(null=True, default=0)
    verdict = models.CharField(max_length=100, default="Wrong Answer")

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return str(self.submitted_at) + " : @" + str(self.user) + " : " + self.problem.title + " : " + self.verdict + " : " + self.language

class TestCase(models.Model):
    problem = models.OneToOneField(Problem, on_delete=models.CASCADE)
    input_data = models.TextField(null=True, blank=True)
    expected_output = models.TextField(null=True, blank=True)

    def __str__(self):#return string representation of object
        return self.problem.title

    




















# class Result(models.Model):
#     submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
#     test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE)
#     status = models.CharField(max_length=50)
#     error_message = models.TextField(blank=True, null=True)