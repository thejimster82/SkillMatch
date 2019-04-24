from datetime import datetime

from django import forms
from django.core.validators import validate_integer
from django.contrib.auth.models import User
from .models import Profile
from django.core.files.images import get_image_dimensions


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class ProfileForm(forms.ModelForm):

    def clean_grad_year(self):
        now = datetime.now().year
        data = self.cleaned_data['grad_year']
        if data < 2019 or data > (now + 5):
            raise forms.ValidationError(
                "Graduation year must be of the form YYYY "
                "and a possible graduation year."
            )
        return data

    class Meta:
        model = Profile
        fields = ('profilePicture', 'gender', 'major', 'bio',
                  'grad_year', 'tutor', 'tutor_gpa', 'tutor_bio')


class ProfileCoursesForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('courses',)
        widgets = {
            'courses': forms.CheckboxSelectMultiple,
        }


class TutorProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('tutor', 'grad_year', 'tutor_gpa', 'tutor_bio')


class BecomeTutorForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('tutor',)
