from django.contrib.auth.models import AnonymousUser
from django.db.models.manager import BaseManager
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth import login, get_user
from django.contrib.auth.forms import UserChangeForm

from datetime import datetime, timedelta, time, date

from .models import Event, EventToEmployee, RepeatedConflict, User, Conflict
from .forms import EventForm, UserCreateForm, ConflictForm, ScheduleForm

# Create your views here.
def make_welcome(request: HttpRequest) -> HttpResponse:
    user = get_user(request)
    if user.username != "":
        today = datetime.today()
        tomorrow = today + timedelta(days=1)
        events = Event.objects.filter(
            start_time__gte=datetime.date(today),
            start_time__lt=datetime.date(tomorrow))
    else:
        events = Event.objects.none()

    employees = []
    for event in events:
        try:
            matches = EventToEmployee.objects.filter(event=event) #!
            names = []
            for match in matches:
                names.append(User.objects.get(id=match.employee.id).first_name)
            employees.append("".join([n+', ' for n in names]))
        except EventToEmployee.DoesNotExist:
            employees.append('NEEDS SCHEDULING')

    context = { 'user': user, 'events': events, 'employees': employees }
    return render(request, 'calender/welcome.html', context)

def make_shifts(request: HttpRequest) -> HttpResponse:
    user = get_user(request)
    if user.username == "":
        context = { 'user': user, 'events': Event.objects.none() }
        return render(request, 'calender/shifts.html', context)

    events = Event.objects.all()
    employees = []
    for event in events:
        try:
            matches = EventToEmployee.objects.filter(event=event) #!
            names = []
            for match in matches:
                names.append(User.objects.get(id=match.employee.id).first_name)
            employees.append("".join([n+', ' for n in names]))
        except EventToEmployee.DoesNotExist:
            employees.append('NEEDS SCHEDULING')

    context = { 'user': user, 'events': events, 'employees': employees }
    return render(request, 'calender/shifts.html', context)

def new_event(request: HttpRequest) -> HttpResponse:
    eventform = EventForm(request.POST or None)

    if request.method == 'POST':
        if eventform.is_valid():
            eventform.save(commit=True)
            return redirect('index')

    context = { 'user': get_user(request), 'event_form': eventform }
    return render(request, 'calender/new_event.html', context)

def delete_event(request: HttpRequest, id: int) -> HttpResponse:
    event = Event.objects.get(id=id)
    event.delete()
    return redirect('view_shifts')

def update_event(request: HttpRequest, id: int) -> HttpResponse:
    user = get_user(request)
    if user.username == "":
        return redirect('index')

    event = Event.objects.get(id=id)
    eventform = EventForm(request.POST or None, instance=event)
    scheduleform = ScheduleForm(request.POST or None)

    if request.method == 'POST':
        if eventform.is_valid():
            eventform.save(commit=True)
        if scheduleform.is_valid():
            data = scheduleform.cleaned_data
            etime = event.start_time
            # Clear the list before replacing it
            EventToEmployee.objects.filter(event=event).delete()
            for employee in data['employees']:
                if not EventToEmployee.objects.filter(employee=employee).exists():
                    conflicts = Conflict.objects.filter(employee=employee)
                    repeat_conflicts = RepeatedConflict.objects.filter(employee=employee)

                    has_conflict = False
                    for conflict in conflicts:
                        if Conflict.is_conflict(conflict, etime):
                            has_conflict = True
                            break
                    if not has_conflict:
                        for conflict in repeat_conflicts:
                            if RepeatedConflict.is_conflict(conflict, etime):
                                has_conflict = True
                                break
                    if not has_conflict:
                        EventToEmployee.objects.create(employee=employee, event=event)
        return redirect('view_shifts')

    context = { 'user': user, 'event_form': eventform, 'schedule_form': scheduleform }
    return render(request, 'calender/update_event.html', context)

def update_conflict(request: HttpRequest) -> HttpResponse:
    user = get_user(request)
    if user.username == "":
        return redirect('index')

    conflictform = ConflictForm(request.POST or None)
    if request.method == 'POST':
        if conflictform.is_valid():
            data = conflictform.cleaned_data
            if data['repeated']:
                for day in data['repeated_days']:
                    repc = RepeatedConflict()
                    start_time: datetime = data['start_time']
                    end_time: datetime = data['end_time']
                    repc.employee = user
                    repc.day = day
                    repc.start_time = start_time
                    repc.end_time = end_time
                    repc.save()
            else:
                conflict = Conflict()
                day: date = datetime.date(data['day'])
                start_time: time = datetime.time(data['start_time'])
                end_time: time = datetime.time(data['end_time'])
                conflict.employee = user
                conflict.start_time = datetime.combine(day, start_time)
                conflict.end_time = datetime.combine(day, end_time)
                conflict.save()
            conflictform = ConflictForm()

    conflicts = Conflict.objects.filter(employee=user)
    rc = RepeatedConflict.objects.filter(employee=user)

    context = { 'user': user, 'repeat_conflicts': rc, 'conflicts': conflicts, 'conflict_form': conflictform }
    return render(request, 'calender/update_conflict.html', context)

def delete_conflict_rc(request: HttpRequest, id: int) -> HttpResponse:
    RepeatedConflict.objects.get(id=id).delete()
    return redirect('update_conflict')

def delete_conflict_c(request: HttpRequest, id: int) -> HttpResponse:
    Conflict.objects.get(id=id).delete()
    return redirect('update_conflict')

def new_user(request: HttpRequest) -> HttpResponse:
    userform = UserCreateForm(request.POST or None)

    if request.method == 'POST':
        if userform.is_valid():
            newuser = userform.save(commit=True)
            login(request, newuser)
            return redirect('index')

    context = { 'user': get_user(request), 'user_form': userform }
    return render(request, 'calender/new_user.html', context)

def make_user(request: HttpRequest) -> HttpResponse:
    user = get_user(request)
    if user.username == "":
        return redirect('new_user')

    userform = UserChangeForm(request.POST or None, instance=user)
    if request.method == 'POST':
        userform.save(commit=True)
        return redirect('index')

    context = { 'user': user, 'user_form': userform }
    return render(request, 'calender/modify_user.html', context)
