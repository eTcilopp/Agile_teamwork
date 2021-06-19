from django import forms
from .models import Post, Comment, Reason, Video
from django.core.files.images import get_image_dimensions


class CommentForm(forms.ModelForm):
    """
    Класс определяет форму создания комментария
    Класс наследутеся от класса встроенной формы ModelForm,
    переопределяя значение атрибута 'class' на 'form-control'
    Вложенный класс Meta определяет сбязанную модель и задает выводимое поле:
    'text'
    """

    def __int__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Comment
        fields = ('text',)


class PostCreationForm(forms.ModelForm):
    """
    Класс определяет форму создания статьи
    Класс наследутеся от класса встроенной формы ModelForm,
    переопределяя значение атрибута 'class' на 'form-control'
    Вложенный класс Meta определяет сбязанную модель и задает выводимое поле:
    'title', 'text', 'category_id'
    """

    def __int__(self, *args, **kwargs):
        super(PostCreationForm, self).__int__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    class Meta:
        model = Post
        fields = ('title',
                  'text',
                  'category_id',
                  'title_photo')


class ReasonCreateForm(forms.ModelForm):
    """
    Класс определяет форму создания статьи
    Класс наследутеся от класса встроенной формы ModelForm,
    переопределяя значение атрибута 'class' на 'form-control'
    Вложенный класс Meta определяет сбязанную модель и задает выводимое поле:
    'title', 'text', 'category_id'
    """

    def __int__(self, *args, **kwargs):
        super(ReasonCreateForm, self).__int__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    class Meta:
        model = Reason
        fields = ('text',)


class VideoCreationForm(forms.ModelForm):
    """
    Test
    """

    def __int__(self, *args, **kwargs):
        super(VideoCreationForm, self).__int__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    class Meta:
        model = Video
        fields = ('title',
                  'file')
