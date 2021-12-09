from django.contrib.auth.models import AnonymousUser
from django.db.models.manager import BaseManager
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth import login, logout, get_user
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

import time
from datetime import datetime

from .models import Event, EventToEmployee, User
from .forms import EventForm

# Create your views here.
def make_welcome(request: HttpRequest) -> HttpResponse:
    user = get_user(request)
    events = Event.objects.all() if user.username != "" else Event.objects.none()

    employees = []
    for event in events:
        try:
            matches = EventToEmployee.objects.get(event=event.id) #!
            names = []
            for match in matches:
                names.append(User.objects.get(id=match.employee).first_name)
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

    context = { 'user': get_user(request), 'events': events }
    return render(request, 'calender/shifts.html', context)

def new_event(request: HttpRequest) -> HttpResponse:
    event = EventForm(request.POST or None)

    if request.method == 'POST':
        if event.is_valid():
            event.save(commit=True)
            return redirect('index')

    context = { 'user': get_user(request), 'event_form': event }
    return render(request, 'calender/new_event.html', context)

def new_user(request: HttpRequest) -> HttpResponse:
    userform = UserCreationForm(request.POST or None)

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
