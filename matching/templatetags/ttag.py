# myproject/myproject/templatetags/tags.py

from django import template
from django.contrib.auth.models import User
from matching.models import MatchesTable

register = template.Library()


@register.simple_tag
def uname(request):
    return User.objects.get(username=request.user.username)


@register.filter(name='common_courses')
def common_courses(match):
    if isinstance(match, MatchesTable):
        from_courses = match.from_user.profile.get_courses()
        to_courses = match.to_user.profile.get_courses()
        common_courses = from_courses.intersection(to_courses)
        return ', '.join(str(c) for c in common_courses)
    else:
        return ''
