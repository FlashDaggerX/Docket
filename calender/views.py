from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

from .models import Event, EventToEmployee
from .forms import EventForm

# Create your views here.
def make_calender(request: HttpRequest) -> HttpResponse:
    context = { 'shifts': 1 }
    return render(request, 'welcome.htmlx')

def new_event(request: HttpRequest) -> HttpResponse:
    event = EventForm(request.POST or None)

    if request.method == 'POST':
        if event.is_valid():
            event.save().save()
            return redirect('index')

    context = { 'event_form': event }
    return render(request, 'calender/new_event.htmlx', context)
