from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth import login, logout

import time
from datetime import datetime

from .models import Event, EventToEmployee, User
from .forms import EventForm, UserCreateForm

# Create your views here.
def make_calender(request: HttpRequest) -> HttpResponse:
    events = Event.objects.all()

    # event_ids = [e.id for e in events]
    # employee_ids = {}
    # employees = {}
    # for eid in event_ids:
    #     employee_ids[eid] = EventToEmployee.objects.get(event=eid)
    #     employees[eid] = User.objects.get(id=employee_ids[eid])

    employees = []
    for event in events:
        try:
            matches = EventToEmployee.objects.get(event=event.id)
            names = []
            for match in matches:
                names.append(User.objects.get(id=match.employee).first_name)
            employees.append("".join([n+', ' for n in names]))
        except EventToEmployee.DoesNotExist:
            employees.append('NEEDS SCHEDULING')

    context = { 'events': events, 'employees': employees }
    return render(request, 'calender/welcome.htmlx', context)

def new_event(request: HttpRequest) -> HttpResponse:
    event = EventForm(request.POST or None)

    if request.method == 'POST':
        if event.is_valid():
            event.save(commit=True)
            return redirect('index')

    context = { 'event_form': event }
    return render(request, 'calender/new_event.htmlx', context)

def new_user(request: HttpRequest) -> HttpResponse:
    user = UserCreateForm(request.POST or None)

    if request.method == 'POST':
        if user.is_valid():
            newuser = user.save(commit=True)
            login(request, newuser)
            return redirect('index')

    context = { 'user_form': user }
    return render(request, 'calender/new_user.htmlx', context)
