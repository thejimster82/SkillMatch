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

        # def clean_profile_picture(self):
        #     profilePicture = self.cleaned_data['profilePicture']
        #
        #     try:
        #         w, h = get_image_dimensions(profilePicture)
        #
        #         # validate dimensions
        #         max_width = max_height = 300
        #         if w > max_width or h > max_height:
        #             raise forms.ValidationError(
        #                 u'Please use an image that is '
        #                 '%s x %s pixels or smaller.' % (max_width, max_height))
        #
        #         # validate content type
        #         main, sub = profilePicture.content_type.split('/')
        #         if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
        #             raise forms.ValidationError(u'Please use a JPEG, '
        #                                         'GIF or PNG image.')
        #
        #         # validate file size
        #         if len(profilePicture) > (40 * 1024):
        #             raise forms.ValidationError(
        #                 u'Avatar file size may not exceed 40k.')
        #
        #     except AttributeError:
        #         """
        #         Handles case when we are updating the user profile
        #         and do not supply a new avatar
        #         """
        #         pass
        #
        #     return profilePicture
