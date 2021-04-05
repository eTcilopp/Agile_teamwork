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

    def clean_title_photo(self):
        avatar = self.cleaned_data['title_photo']
        filesize = avatar.file.size
        print(filesize)
        megabyte_limit = 0.02
        if filesize > megabyte_limit * 1250 * 700:
            raise forms.ValidationError("Max file size is %sMB" % str(megabyte_limit))
        try:
            w, h = get_image_dimensions(avatar)
            filesize = avatar.file.size
            print(filesize)
            # validate dimensions
            max_width = max_height = 1000
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
