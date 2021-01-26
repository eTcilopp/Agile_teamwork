from django.db import models
from authapp.models import User
import datetime


class CategoryPost(models.Model):
    name = models.CharField(verbose_name='Категория', max_length=30, unique=True)
    slug = models.SlugField(allow_unicode=True, max_length=64)
    description = models.TextField(verbose_name='Описание', max_length=64)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class StatusPost(models.Model):
    CHOICES_STATUS = (('Apr', 'Одобрено'), ('Pub', 'Опубликовано'), ('Del','Удалено'), ('Drf', 'Черновик'))

    name_status = models.CharField(verbose_name='Статус', choices=CHOICES_STATUS, default='Drf', max_length=32,)

    def __str__(self):
        return self.name_status


class Post(models.Model):
    category_id = models.ForeignKey(CategoryPost, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Заголовок', max_length=64)
    slug = models.SlugField(allow_unicode=True, max_length=64)
    text = models.TextField(verbose_name='Содержание')
    status = models.ForeignKey(StatusPost, on_delete=models.PROTECT)
    status_update = models.DateField(verbose_name='Дата обновления статуса', default=datetime.date.today)
    date_create = models.DateField(verbose_name='Дата создания статьи', default=datetime.date.today)
    date_update = models.DateField(verbose_name='Дата изменения статьи', default=datetime.date.today)

    def __str__(self):
        return f'{self.text} ({self.category_id.name}) by {self.user_id.name}'


class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', null=True, blank=True, related_name='ответы', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Комментарий')
    date_create = models.DateField(verbose_name='Дата создания комментария', default=datetime.date.today)
    date_update = models.DateField(verbose_name='Дата изменения комментария', default=datetime.date.today)

    def __str__(self):
        return f'{self.text} by {self.user_id.name} ({self.post_id.name})'


class Like(models.Model):
    author_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Author_like')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, default=None)
    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE, default=None)
    date_create = models.DateField(default=datetime.date.today)
    date_update = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f'{self.post_id.name} ({self.user_id.name})'
