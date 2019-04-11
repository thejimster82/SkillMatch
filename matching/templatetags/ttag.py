# myproject/myproject/templatetags/tags.py

from django import template
from django.contrib.auth.models import User

register = template.Library()


@register.simple_tag
def uname(request):
    return User.objects.get(username=request.user.username)
