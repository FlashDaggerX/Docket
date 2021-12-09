from django.db import models
from django.contrib.auth.models import User

from datetime import datetime

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=100)
    start_time = models.DateTimeField(default=datetime.now().strftime("%D %I:%M%p"))
    end_time = models.DateTimeField(default=datetime.now().strftime("%D %I:%M%p"))

# Keeps a mapping of employees to events
class EventToEmployee(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
