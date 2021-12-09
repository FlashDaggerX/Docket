from django.template.library import Library

register = Library()

# Added for custom array indexing in templates
# https://docs.djangoproject.com/en/3.2/howto/custom-template-tags/
# Don't forget to reboot and {% load index %}
@register.filter
def index(List, i):
    return List[int(i)]
