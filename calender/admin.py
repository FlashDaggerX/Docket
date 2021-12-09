from django.contrib import admin

from .models import Event, EventToEmployee

# Register your models here.
admin.register(Event)
admin.site.register(Event)
admin.register(EventToEmployee)
admin.site.register(EventToEmployee)
