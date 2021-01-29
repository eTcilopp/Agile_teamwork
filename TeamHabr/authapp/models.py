from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime


class User(AbstractUser):
    """
    ТЕКСТ
    :param AbstractUser - ТЕКСТ
    """
    username = models.CharField(verbose_name="Логин", max_length=64, unique=True)
    name = models.CharField(verbose_name="Имя", max_length=64, default='')
    surname = models.CharField(verbose_name="Фамилия", max_length=64, default='')
    status_block = models.BooleanField(default=False, verbose_name="Статус блокировки")
    status_update = models.DateTimeField(verbose_name="Дата смены статуса", default=datetime.datetime.today)
    date_create = models.DateTimeField(verbose_name="Дата создания", default=datetime.datetime.today)
    date_update = models.DateTimeField(verbose_name="Дата редактирования", default=datetime.datetime.today)

    class Meta:
        verbose_name_plural = 'Пользователи'
        verbose_name = 'Пользователь'
        ordering = ['username']

