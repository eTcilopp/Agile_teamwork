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
        verbose_name="Last name",
        max_length=64,
        default='')
    status_block = models.BooleanField(
        default=False,
        verbose_name="Block status")
    status_update = models.DateTimeField(
        verbose_name="Status updated date",
        default=datetime.datetime.today)
    date_create = models.DateTimeField(
        verbose_name="Date created",
        default=datetime.datetime.today)
    date_update = models.DateTimeField(
        verbose_name="Date updated",
        default=datetime.datetime.today)
    email = models.EmailField(
        blank=True,
        unique=True,
        max_length=254,
        verbose_name="Email")
    avatar = models.ImageField(
        blank=True,
        upload_to="users_avatars/",
        verbose_name="Avatar")
    age = models.PositiveIntegerField(
        verbose_name="Age",
        default=0)
    aboutMe = models.TextField(
        verbose_name="About me",
        max_length=512,
        blank=True)

    class Meta:
        verbose_name_plural = 'User'
        verbose_name = 'Users'
        ordering = ['username']
