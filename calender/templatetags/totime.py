from django.template.library import Library
from django.template.defaultfilters import stringfilter

import pytz
from datetime import datetime

register = Library()

@register.filter
def totime(date: datetime, t: int):
    if t == 0:
        return date.astimezone(pytz.timezone('America/New_York')).strftime("%I:%m %p")
    elif t == 1:
        return date.astimezone(pytz.timezone('America/New_York')).strftime("%m/%d/%Y")
