from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from django import forms
from .models import User


class UserLoginForm(AuthenticationForm):

    """
    Класс определяет форму авторизации пользователя.
    Форма наследуется от встроенного класса AuthenticationForm,
    переопределяя значение атрибута 'class' на 'form-control'
    Вложенный класс Meta определяет выводимые поля формы: "username", "password"
    """

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = User
        fields = ("username",
                  "password")


class UserRegisterForm(UserCreationForm):
    """
    Класс определяет форму регистрации пользователя.
    Форма наследуется от встроенного класса UserCreationForm,
    переопределяя значение атрибута 'class' на 'form-control'
    Вложенный класс Meta определяет выводимые поля формы:
    "username", "name", "surname", "password1", "password2", "email"
    """

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.help_text = ""

    class Meta:
        model = User
        fields = (
            "username",
            "name",
            "surname",
            "password1",
            "password2",
            "email")
