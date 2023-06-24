from django.contrib.auth import authenticate, login
from .forms import UserLoginForm
from django.shortcuts import render, redirect,get_object_or_404
from .models import Problem 
# Create your views here.


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
    return render(request, 'judge/login.html', {'form': form})

# def register(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')
#     else:
#         form = RegistrationForm()
#     return render(request, 'registration.html', {'form': form})

def problems(request):
    problems = Problem.objects.all()  # Retrieve all problems from the Problem model
    return render(request, 'problems.html', {'problems': problems})

def problem_description(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    return render(request, 'problem_description.html', {'problem': problem})

def compile_code(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    
    if request.method == 'POST':
        code = request.POST.get('code')
        language = request.POST.get('language')
        
        # Execute the user's code based on the selected language
        # Add your code execution logic here
        
        # Store the result or any relevant information for display in the template
        result = "Code execution result"
        
        return render(request, 'compile_result.html', {'problem': problem, 'result': result})

    return render(request, 'problem_description.html', {'problem': problem})