from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from django import forms
from .models import User
from django.core.files.images import get_image_dimensions
import re


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
            if field_name == "username":
                field.widget.attrs["minlength"] = 4
            if field_name == "name" or field_name == "surname":
                field.widget.attrs["minlength"] = 2

    def clean_username(self):
        username = self.cleaned_data['username']
        if not username[0].isalpha():
            raise forms.ValidationError('Логин должен начинаться с буквы')
        for let in username:
            if not re.search(r'\w', let):
                raise forms.ValidationError('Логин может содержать только буквы, цифры и _')
        return username

    def clean_name(self):
        name = self.cleaned_data['name']
        if not name.isalpha():
            raise forms.ValidationError('Имя может быть только из букв')
        return name

    def clean_surname(self):
        surname = self.cleaned_data['surname']
        if not surname.isalpha():
            raise forms.ValidationError('Фамилия может быть только из букв')
        return surname

    class Meta:
        model = User
        fields = (
            "username",
            "name",
            "surname",
            "password1",
            "password2",
            "email")


class UserEditForm(UserChangeForm):
    """
    Класс определяет форму изменения данных пользователя.
    Форма наследуется от встроенного класса UserChangeForm,
    переопределяя значение атрибута 'class' на 'form-control'
    Вложенный класс Meta определяет выводимые поля формы:
    "username", "name", "surname", "password", "email"
    """

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']
        try:
            w, h = get_image_dimensions(avatar)
            # validate dimensions
            max_width = max_height = 100
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    u'Please use an image that is '
                    '%s x %s pixels or smaller.' % (max_width, max_height))
            # validate content type
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, '
                                            'GIF or PNG image.')
            # validate file size
            if len(avatar) > (20 * 1024):
                raise forms.ValidationError(
                    u'Avatar file size may not exceed 20k.')
        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass
        return avatar

    class Meta:
        model = User
        fields = (
            "username",
            "name",
            "surname",
            "age",
            "aboutMe",
            "password",
            "email",
            "avatar",
        )
