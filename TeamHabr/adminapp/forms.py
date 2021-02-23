from django import forms
from mainapp.models import CategoryPost


class CategoryCreationForm(forms.ModelForm):
    """
    Класс определяет форму создания статьи
    Класс наследутеся от класса встроенной формы ModelForm,
    переопределяя значение атрибута 'class' на 'form-control'
    Вложенный класс Meta определяет сбязанную модель и задает выводимое поле:
    'title', 'text', 'category_id'
    """

    def __int__(self, *args, **kwargs):
        super(CategoryCreationForm, self).__int__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    class Meta:
        model = CategoryPost
        fields = ('name',
                  'description')

