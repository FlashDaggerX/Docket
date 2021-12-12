from datetime import datetime
from django import forms

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm

from .models import Event, Conflict

DAYS = (
    ('Sunday', 'Sunday'),
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
)

class EventForm(forms.ModelForm):
    start_time = forms.DateTimeField(
        input_formats=['%m/%d/%Y %I:%M %p'],
        widget=forms.widgets.DateTimeInput(
            format="%m/%d/%Y %I:%M %p",
            attrs={'class': 'form-control datetimepicker-input',
                    'data-target': '#datetimepicker1',
                    'placeholder':"MM/DD/YY HH:MM(AP)"}))
    end_time = forms.DateTimeField(
        input_formats=['%m/%d/%Y %I:%M %p'],
        widget=forms.widgets.DateTimeInput(
            format="%m/%d/%Y %I:%M %p",
            attrs={'class': 'form-control datetimepicker-input',
                    'data-target': '#datetimepicker2',
                    'placeholder':"MM/DD/YY HH:MM(AP)"}))
    class Meta:
        model = Event
        fields = "__all__"

class ScheduleForm(forms.Form):
    employees = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(is_superuser=False))

class ConflictForm(forms.Form):
    repeated = forms.BooleanField(
        required=False)
    repeated_days = forms.MultipleChoiceField(
        required=False,
        choices=DAYS)
    day = forms.DateTimeField(
        input_formats=['%m/%d/%Y'],
        initial=datetime.now,
        widget=forms.widgets.DateInput(
            format="%m/%d/%Y",
            attrs={'class': 'form-control datetimepicker-input',
                    'data-target': '#datetimepicker1',
                    'placeholder':"MM/DD/YY"}))
    start_time = forms.DateTimeField(
        required=True,
        input_formats=['%I:%M %p'],
        widget=forms.widgets.TimeInput(
            format="%I:%M %p",
            attrs={'class': 'form-control datetimepicker-input',
                    'data-target': '#datetimepicker2',
                    'placeholder':"HH:MM(AP)"}))
    end_time = forms.DateTimeField(
        required=True,
        input_formats=['%I:%M %p'],
        widget=forms.widgets.TimeInput(
            format="%I:%M %p",
            attrs={'class': 'form-control datetimepicker-input',
                    'data-target': '#datetimepicker3',
                    'placeholder':"HH:MM(AP)"}))
    # class Meta:
    #     model = Conflict
    #     fields = ('start_time', 'end_time')
    #     exclude = ('employee')

# # https://stackoverflow.com/a/28897968
class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name' , 'last_name')

class UserAdmin(UserAdmin):
    add_form = UserCreateForm
    prepopulated_fields = {'username': ('first_name' , 'last_name')}

    # https://stackoverflow.com/a/53237541
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'username', 'password1', 'password2', ),
        }),
    )

# Re-register user models to add new fields
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
