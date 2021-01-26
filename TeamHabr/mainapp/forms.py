from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from django import forms
from .models import Post, Comment


class CommentForm(forms.ModelForm):

    """
    ТЕКСТ
    :param CommentForm - ТЕКСТ
    """

    def __int__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Comment
        fields = 'text'


class PostCreationForm(forms.ModelForm):
    """
    ТЕКСТ
    :param PostCreationForm - ТЕКСТ
    """
    def __int__(self, *args, **kwargs):
        super(PostCreationForm, self).__int__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    class Meta:
        model = Post
        fields = ('title', 'text')
