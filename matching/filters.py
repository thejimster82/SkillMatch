from .models import Profile
import django_filters

class TutorFilter(django_filters.FilterSet):
    gpa_gt = django_filters.NumberFilter(field_name='tutor_gpa', lookup_expr='gt')
    grad_year = django_filters.CharFilter(field_name='grad_year')