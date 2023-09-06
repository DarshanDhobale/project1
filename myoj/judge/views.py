from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .forms import UserLoginForm,CodeSubmissionForm
from django.shortcuts import render, redirect,get_object_or_404
from .models import Problem , Submission,TestCase,Userprofile
from datetime import datetime
from time import time

import os
import signal
import subprocess
import os.path
import docker

# Create your views here.

def homeview(request):
    return render(request, 'home.html')

#sign is called twice to signup a new
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('problems')  # Replace 'problems' with the desired URL name to redirect after successful signup
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def problems(request):
    problems = Problem.objects.all()  # Retrieve all problems from the Problem model
    return render(request, 'problems.html', {'problems': problems})

@login_required(redirect_field_name="login")
def problem_description(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    return render(request, 'problem_description.html', {'problem': problem})

def leaderboard(request):
    objects=Userprofile.objects.all()
    return render(request, 'leaderboard.html', {'objects': objects})

def dashboard(request):
    user_profile = Userprofile.objects.get(user=request.user)
    return render(request, 'dashboard.html', {'user_profile': user_profile})

@login_required(redirect_field_name="login")
def compile_code(request, problem_id):
    if request.method == 'POST':

        docker_client = docker.from_env()
        Running = "running"

        problem = Problem.objects.get(id=problem_id)
        testcase = TestCase.objects.get(problem_id=problem_id)
        
        testcase.expected_output = testcase.expected_output.replace('\r\n','\n').strip() 

        if problem.difficulty=="Easy":
            score = 2
        elif problem.difficulty=="Medium":
            score = 4
        else:
            score = 8

        verdict = "Wrong Answer" 
        res = ""
        run_time = 0

        form = CodeSubmissionForm(request.POST)
        code = ''
        if form.is_valid():
            code = form.cleaned_data.get('code')
            code = code.replace('\r\n','\n').strip()

        language = request.POST['language']
        submission = Submission(user=request.user, problem=problem, submitted_at=datetime.now(), 
                                    language=language, code=code)
        
        submission.save()
        filename = str(submission.id)
        # if user code is in C++
        if language == "C++":
            extension = ".cpp"
            cont_name = "suspicious_grothendiec"
            compile = f"g++ -o {filename} {filename}.cpp" #f is used to embed expressions inside string
            clean = f"{filename} {filename}.cpp"
            docker_img = "gcc"
            exe = f"./{filename}"

        elif language == "Python":
            extension = ".py"
            cont_name = "jovial_liskov"
            compile = "python"
            clean = f"{filename}.py"
            docker_img = "python"
            exe = f"python {filename}.py"
        
        
        file = filename + extension
        filepath = os.path.join(settings.MEDIA_ROOT, file)
        
        try:
            with open(filepath, "w") as code_file:
                code_file.write(code)
                
        except Exception as e:
            print(f"Error writing file: {e}")
            

        try:
            container = docker_client.containers.get(cont_name)
            container_state = container.attrs['State']
            container_is_running = (container_state['Status'] == Running)
            if not container_is_running:
                subprocess.run(f"docker start {cont_name}",shell=True)
        except docker.errors.NotFound:
            subprocess.run(f"docker run -dt --name {cont_name} {docker_img}",shell=True)


        # copy/paste the  file in docker container 
        subprocess.run(f"docker cp {filepath} {cont_name}:/{file}",shell=True)
        # compiling the code
        cmp = subprocess.run(f"docker exec {cont_name} {compile}", capture_output=True, shell=True)
        if cmp.returncode != 0:
            verdict = "Compilation Error"
            subprocess.run(f"docker exec {cont_name} rm {file}",shell=True)

        else:
            # running the code on given input and taking the output in a variable in bytes
            start = time()
            try:
                command = [ r"C:\\Program Files\\Docker\\Docker\\resources\\bin\\docker.exe",
                            "exec",
                            cont_name,
                            "sh",
                            "-c",
                            f"echo '{testcase.input_data}' | {exe}"
                          ]
                res = subprocess.run(command, capture_output=True, timeout=problem.time_limit, shell=True)
                run_time = time()-start
                subprocess.run(f"docker exec {cont_name} rm {clean}",shell=True)
            except subprocess.TimeoutExpired:
                run_time = time()-start
                verdict = "Time Limit Exceeded"
                subprocess.run(f"docker container kill {cont_name}", shell=True)
                subprocess.run(f"docker start {cont_name}",shell=True)
                subprocess.run(f"docker exec {cont_name} rm {clean}",shell=True)
            except Exception as e:
                verdict = "Runtime Error"
                context = {'verdict': verdict, 'error': str(e)}
                return render(request, 'result.html', context)

            else:
                if res.returncode != 0:
                    verdict = "Runtime Error"
                    context = {'verdict': verdict, 'error': res.stderr.decode('utf-8')}
                    return render(request, 'result.html', context)
                

        user_stderr = ""
        user_stdout = ""
        if verdict == "Compilation Error":
            user_stderr = cmp.stderr.decode('utf-8')
            
        elif verdict == "Wrong Answer":
            user_stdout = res.stdout.decode('utf-8')
            
            if str(user_stdout)==str(testcase.expected_output):
                verdict = "Accepted"
                
            testcase.expected_output += '\n' # added extra line to compare user output having extra ling at the end of their output
            if str(user_stdout)==str(testcase.expected_output):
                verdict = "Accepted"
        
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                print(f"File removed successfully: {filepath}")
            except Exception as e:
                print(f"Error removing file: {e}")
        else:
            print(f"File does not exist: {filepath}")

        # Assuming you have the username of the currently logged-in user
        username = request.user  # Replace with the actual username

        # Get the User object
        user = User.objects.get(username=username)

        # Fetch the UserProfile associated with the User
        user_profile = Userprofile.objects.get(user=user)

        previous_verdict = Submission.objects.filter(user=user.id, problem=problem, verdict="Accepted")
        if len(previous_verdict)==0 and verdict=="Accepted":
            user_profile.total_score += score
            user_profile.total_solved += 1
            user_profile.save()

        submission.verdict = verdict
        submission.user_stdout = user_stdout
        submission.user_stderr = user_stderr
        submission.run_time = run_time
        submission.save()
        context = {'verdict': verdict, 'user_stderr': user_stderr ,'user_stdout':user_stdout}
        return render(request,'result.html',context)
