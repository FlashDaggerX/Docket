from django.db import models
from django.contrib.auth.models import User

from datetime import datetime, time, date

def _timenow():
    return datetime.time(datetime.now())

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=100)
    start_time = models.DateTimeField(default=datetime.now)
    end_time = models.DateTimeField(default=datetime.now)

# A block of time which the employee can't be scheduled for
class Conflict(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=datetime.now)
    end_time = models.DateTimeField(default=datetime.now)

    def is_conflict(obj, date: datetime) -> bool:
        st: datetime = obj.start_time
        et: datetime = obj.end_time
        return not st < date < et

class RepeatedConflict(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.CharField(max_length=10)
    start_time = models.TimeField(default=_timenow)
    end_time = models.TimeField(default=_timenow)

    def is_conflict(obj, date: datetime) -> bool:
        st: time = obj.start_time
        et: time = obj.end_time

        totime = lambda d: datetime.time(d)
        return date.strftime("%A") == obj.day and not totime(st) < totime(date) < totime(et)

# Keeps a mapping of employees to events
class EventToEmployee(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
