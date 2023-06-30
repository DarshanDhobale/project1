from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
# Create your models here.

class Userprofile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    total_questions= models.IntegerField(default=0)
    total_score= models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
    

class Problem(models.Model):
    DIFFICULTY_CHOICES = [('Easy', 'Easy'),('Medium', 'Medium'),('Hard', 'Hard'),]
    DEFAULT_DIFFICULTY = 'Easy'
    title = models.CharField(max_length=255)
    statement = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES ,null=True)

    def __str__(self):
        return self.title

class Submission(models.Model):
    LANGUAGE_CHOICES = [('C++', 'C++'),('Python', 'Python'),('Java', 'Java'),]
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.TextField()
    language = models.CharField(max_length=10, choices= LANGUAGE_CHOICES)
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