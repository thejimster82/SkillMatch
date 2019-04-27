from datetime import datetime

from django import forms
from django.core.validators import validate_integer
from django.contrib.auth.models import User
from .models import Profile
from django.core.files.images import get_image_dimensions

from dal import autocomplete


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class ProfileForm(forms.ModelForm):

    def clean_grad_year(self):
        now = datetime.now().year
        data = self.cleaned_data['grad_year']
        if data < now or data > (now + 5):
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
            'courses': autocomplete.ModelSelect2Multiple(url='course-autocomplete'),
        }


class TutorProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('tutor', 'tutor_gpa', 'tutor_bio')

    def clean_tutor_gpa(self):
        data = self.cleaned_data['tutor_gpa']
        print('data', data)
        if data < 0 or data > 4.0:
            raise forms.ValidationError(
                "GPA must be between 0.0 and 4.0 "
            )
        return data


class BecomeTutorForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('tutor',)
