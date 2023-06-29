from django import template  
register = template.Library()
from cutomuser.models import Workarea,Application

@register.filter()
def set(value,arg):
    value = arg
    return value

@register.simple_tag
def my_workarea(user):
    wk = Workarea.objects.all()
    for i in wk:
        if user in  i.members.all():
            return  i
    return  0

@register.simple_tag
def slots(job):
    apps = Application.objects.filter(job=job)
    if apps:
        return 30-apps.count()
    return 30

@register.simple_tag
def mod(value):
    return value%7

@register.simple_tag
def get_colors(colors,id):
    for i in range(len(colors)):
        if int(id) == i:
            return colors[i]
    return colors[0]