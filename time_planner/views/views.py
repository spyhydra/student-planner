from pyexpat.errors import messages

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LoginForm
from ..models import Task, User


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after signup
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    user_id = request.session.get('user_id')
    if user_id is not None:
        return redirect('/')
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.filter(email=email, password=password).first()
            if user:

                # Login successful

                request.session['user_id'] = user.id
                print("user id", user.id)
                render(request, 'index.html', {'user': user})
                return redirect('/')
            else:
                messages.error(request, "Invalid credentials")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def add_and_show_tasks(request):
    user_id = request.session.get('user_id')
    if user_id is not None:
        user = User.objects.get(pk=user_id)
        if request.method == "POST":
            title = request.POST.get("title")
            priority = request.POST.get("priority")
            due_date = request.POST.get("due_date")
            Task.objects.create(title=title, priority=priority, user=user, due_date=due_date)

        tasks = Task.objects.filter(user=user)
        return render(request, "add_task.html", {"tasks": tasks})
    else:
        return redirect('login')


#dashboard view
def dashboard(request):
    user_id = request.session.get('user_id')
    print("enter in dashboard")
    if user_id is not None:
        print("user id", user_id)
        # User is logged in, retrieve user data and display dashboard
        user = User.objects.get(pk=user_id)
        tasks = Task.objects.filter(user=user)

        return render(request, "index.html", {"tasks": tasks})
    else:
        return redirect('login')


#show the task and show the task
def show_tasks(request):
    print("enter in show task"
          )
    user_id = request.session.get('user_id')

    user = User.objects.get(pk=user_id)

    tasks = Task.objects.filter(user=user)  # Get all tasks of the logged in user

    return render(request, "show_task.html", {"tasks": tasks})


#complete task
def complete_task(request, id):
    task = Task.objects.get(pk=id)
    task.completed = True
    task.save()
    return redirect('task')


#delete task
def delete_task(request, id):
    Task.objects.get(pk=id).delete()
    return redirect('task')

#logout the user
def logout(request):
    del request.session['user_id']
    return redirect('login')

