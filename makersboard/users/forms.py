from django import forms

from .models import UserProfile


class UserForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'profile_picture',
            'first_name',
            'last_name',
            'phone_number',
            'username',
            'email',
            'password',
        ]


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'profile_picture',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'password',
        ]


class UserLoginForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'username',
            'password',
        ]
