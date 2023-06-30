from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .forms import UserLoginForm,CodeSubmissionForm
from django.shortcuts import render, redirect,get_object_or_404
from .models import Problem , Submission


# Create your views here.

def homeview(request):
    return render(request, 'home.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('problems')  # Replace 'home' with the desired URL name to redirect after successful signup
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('problems')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

# def register(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')
#     else:
#         form = RegistrationForm()
#     return render(request, 'registration.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


def problems(request):
    problems = Problem.objects.all()  # Retrieve all problems from the Problem model
    return render(request, 'problems.html', {'problems': problems})


def problem_description(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    return render(request, 'problem_description.html', {'problem': problem})

@login_required(redirect_field_name="login")
def compile_code(request, problem_id):
    if request.method == 'POST':
        form = CodeSubmissionForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            user = request.user
            problem = Problem.objects.get(pk=problem_id)
            language = form.cleaned_data['language']
            
            # Create a new Submission instance
            submission = Submission.objects.create(
                problem=problem,
                user=user,
                code=code,
                language=language,
            )
            submission.save()
            # Perform any additional processing or actions
            
            return redirect('compile_result.html')
    else:
        form = CodeSubmissionForm()
    
    return render(request,'judge/compile_code.html', {'form': form})
