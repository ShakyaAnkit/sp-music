from django import template
from django.contrib.auth.models import Group 

register = template.Library() 

@register.filter 
def get_time(progress):
    seconds = (progress/1000) % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)