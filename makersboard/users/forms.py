from django import forms

from .models import UserProfile


class UserForm(forms.ModelForm):
    class Meta:
        password = forms.CharField(widget=forms.PasswordInput)
        model = UserProfile
        widgets = {
            'password': forms.PasswordInput(),
        }
        fields = [
            'profile_picture',
            'first_name',
            'last_name',
            'username',
            'password',
            'email',
            'phone_number',
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
        ]
