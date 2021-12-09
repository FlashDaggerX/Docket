from django import forms

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
