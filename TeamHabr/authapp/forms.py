from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm

from django import forms
from .models import User


class UserLoginForm(AuthenticationForm):
    """
    ТЕКСТ
    :param AuthenticationForm - ТЕКСТ
    """
    class Meta:
        model = User
        fields = ("username", "password")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class UserRegisterForm(UserCreationForm):
    """
    ТЕКСТ
    :param AuthenticationForm - ТЕКСТ
    """
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.help_text = ""

    class Meta:
        model = User
        fields = ("username", "name", 'surname', "password1", "password2", "email")