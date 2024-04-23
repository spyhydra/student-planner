from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.contrib import messages
from ..models import User, Task
from django.http import HttpResponse, HttpRequest


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            print("data entered")
            form.save()
            messages.success(request, 'Your account has been created')
            return redirect('login')  # Redirect to login page after signup
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.filter(email=email, password=password).first()
            if user:
                # Login successful
                messages.success(request, 'Logged in successfully')
                return HttpResponse("Login Successful")
            else:
                messages.error(request, "Invalid credentials")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def add_and_show_tasks(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        title = request.POST.get("title")
        priority = request.POST.get("priority")
        Task.objects.create(title=title, priority=priority)


    return render(request, "add_task.html")


def show_tasks(request: HttpRequest) -> HttpResponse:
    tasks = Task.objects.all()
    return render(request, "task.html", {"tasks": tasks})

def dashboard(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")
