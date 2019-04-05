from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.core.files.images import get_image_dimensions


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profilePicture', 'gender', 'major', 'courses', 'bio',
                  'grad_year', 'tutor', 'tutor_gpa', 'tutor_bio')


class BecomeTutorForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('tutor')
