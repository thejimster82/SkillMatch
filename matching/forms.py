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
        fields = ('gender', 'major', 'bio', 'grad_year', 'profilePicture')
