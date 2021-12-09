from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm

from .models import Event

class EventForm(forms.ModelForm):
    start_time = forms.DateTimeField(
        input_formats=['%m/%d/%y %I:%M%p'],
        widget=forms.widgets.DateTimeInput(
            format="%m/%d/%y %I:%M%p",
            attrs={'placeholder':"MM/DD/YY HH:MM(AP)"}))
    end_time = forms.DateTimeField(
        input_formats=['%m/%d/%y %I:%M%p'],
        widget=forms.widgets.DateTimeInput(
            format="%m/%d/%y %I:%M%p",
            attrs={'placeholder':"MM/DD/YY HH:MM(AP)"}))
    class Meta:
        model = Event
        fields = "__all__"

# https://stackoverflow.com/a/28897968
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
