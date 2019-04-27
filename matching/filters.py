from .models import Profile
import django_filters

class TutorFilter(django_filters.FilterSet):
    class Meta:
        model = Profile
        fields = ['tutor_gpa', 'grad_year', ]