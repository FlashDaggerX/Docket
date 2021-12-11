from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm

from .models import Event, Conflict

class EventForm(forms.ModelForm):
    start_time = forms.DateTimeField(
        input_formats=['%m/%d/%y %I:%M%p'],
        widget=forms.widgets.DateTimeInput(
            format="%m/%d/%y %I:%M%p",
            attrs={'class': 'form-control datetimepicker-input',
                    'data-target': '#datetimepicker1',
                    'placeholder':"MM/DD/YY HH:MM(AP)"}))
    end_time = forms.DateTimeField(
        input_formats=['%m/%d/%y %I:%M%p'],
        widget=forms.widgets.DateTimeInput(
            format="%m/%d/%y %I:%M%p",
            attrs={'class': 'form-control datetimepicker-input',
                    'data-target': '#datetimepicker2',
                    'placeholder':"MM/DD/YY HH:MM(AP)"}))
    class Meta:
        model = Event
        fields = "__all__"

class ConflictForm(forms.Form):
    repeated = forms.BooleanField()
    repeated_days = forms.CheckboxSelectMultiple()
    # class Meta:
    #     model = Conflict
    #     fields = ('start_time', 'end_time')
    #     exclude = ('employee')
