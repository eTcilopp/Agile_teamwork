from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime


class User(AbstractUser):
    """
    Класс модели Пользователя.
    Класс наследуется от встроенного класса AbstractUser.
    Задаются поля таблицы базы данных:
    username - логин пользователя,
    name - имя пользователя,
    surname - фамилия пользователя,
    status_block - булевое значение, определяющее, заблокирован ли пользователь:
        True - пользователь заблокирован
        False - пользователь не заблокирован
    status_update - дата последнего изменения статуса блокировки пользователя,
    date_create - дата создания учетной записи пользователя,
    date_update - дата любого изменения параметров учетной записи пользователя.

    Вложенный класс Meta определяет наименование полей формы в разделе администрирования,
    а также принцип сортировки вывода списка пользователей (по логину, по убыванию)
    """
    username = models.CharField(
        verbose_name="Логин",
        max_length=64,
        unique=True)
    name = models.CharField(verbose_name="Имя", max_length=64, default='')
    surname = models.CharField(
        verbose_name="Фамилия",
        max_length=64,
        default='')
    status_block = models.BooleanField(
        default=False,
        verbose_name="Статус блокировки")
    status_update = models.DateTimeField(
        verbose_name="Дата смены статуса",
        default=datetime.datetime.today)
    date_create = models.DateTimeField(
        verbose_name="Дата создания",
        default=datetime.datetime.today)
    date_update = models.DateTimeField(
        verbose_name="Дата редактирования",
        default=datetime.datetime.today)

    class Meta:
        verbose_name_plural = 'Пользователи'
        verbose_name = 'Пользователь'
        ordering = ['username']
