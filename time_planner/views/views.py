from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.contrib import messages
from ..models import User, Task
from django.http import HttpResponse, HttpRequest
from calendar import monthrange, monthcalendar
from datetime import datetime,timedelta


def calendar_view(request, year=datetime.now().year, month=datetime.now().month):
    # Get current date and calculate first day of the month
    now = datetime(year, month, 1)
    first_day = now.weekday()

    # Get month calendar data
    month_calendar = monthcalendar(year, month)

    # Get events for the month (if using Event model)
    events = []  # Replace with query to fetch events for the month
    if Event:
        events = Event.objects.filter(date__year=year, date__month=month)

    # Prepare context dictionary
    context = {
        'year': year,
        'month': month,
        'month_name': now.strftime('%B'),
        'month_calendar': month_calendar,
        'first_day': first_day,
        'events': events,  # Add events list if using
    }

    return render(request, 'calendar_app/calendar.html', context)

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
    return render(request, "show_task.html", {"tasks": tasks})


def dashboard(request: HttpRequest) -> HttpResponse:
    tasks = Task.objects.all()
    count = Task.objects.count()
    print("count is: ", count)
    return render(request, "index.html", {"tasks": tasks})


#temp model
def show_task(request: HttpRequest, id: int) -> HttpResponse:
    task = Task.objects.get(id=id)

    return render(request, "show_task.html", {"task": task})


def delete_task(request: HttpRequest, id: int) -> HttpResponse:
    task = Task.objects.get(id=id)
    print("you deleted id is: ", task)
    task.delete()
    return redirect('/show-task/')
