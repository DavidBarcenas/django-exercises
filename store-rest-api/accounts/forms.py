from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.utils.translation import gettext as _
from django import forms

from accounts.models import UserProfile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=50,
        error_messages={
            'invalid': _('Entered a valid email.')
        }
    )

    def save(self):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1'],
        )

        return user

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        emailExists = User.objects.filter(email=email)

        if emailExists.count():
            raise ValidationError('This email already exists!.')

        return email


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('avatar', 'user')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

        self.fields['user'].widget = forms.HiddenInput()
        self.fields['user'].required = False

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']
        width, height = get_image_dimensions(avatar)

        max_width = 2000
        max_height = 2000

        if width > max_width or height > max_height:
            raise forms.ValidationError(
                'The image must not exceed %spx %spx' % (max_width, max_height))

        file, type = avatar.content_type.split('/')

        if not(file == 'image' and type in ['jpeg', 'jpg', 'gif', 'png']):
            raise forms.ValidationError('This file is not supported.')

        if len(avatar) > (300 * 1024):
            raise forms.ValidationError('The image must not exceed 30kb.')

        return avatar
