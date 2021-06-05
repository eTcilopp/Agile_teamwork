from django.core.exceptions import ValidationError
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.timezone import utc
from django.db import models
from django.urls import reverse
from django.conf import settings
from authapp.models import User
import datetime
from slugify import slugify
from ckeditor_uploader.fields import RichTextUploadingField

now = datetime.datetime.now().replace(tzinfo=utc)


def valid_photo(photo):
    """
    Функция валидации размера фото
    :param photo: принимает фотографию
    :return: ошибку в случае провала валидации
    """
    filesize = photo.file.size
    megabyte_limit = 0.9
    if filesize > megabyte_limit * 1250 * 700:
        raise ValidationError(f"Максимальный размер картинки {megabyte_limit}MB и размеры 1250 * 700")


class CategoryPost(models.Model):
    """
    Класс модели перечня категорий статей.
    Класс наследуется от встроенного класса Model.
    Задаются поля таблицы базы данных:
    name - наименование категории
    slug - слаг наименования категории,
    is_active - булевое значение активности категорииЖ
        True - категория активна
        False - категория не активка
    """

    name = models.CharField(
        verbose_name='Category',
        max_length=30,
        unique=True)
    slug = models.SlugField(
        allow_unicode=True,
        max_length=64,
        editable=False,
        unique=True)
    description = models.TextField(verbose_name='Descriprion', max_length=64)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Переопределение метода Save класса CategoryPost
        При вызове метода save выполняется провекра - заполнено ли поле slug у данной категории.
        Если не заполнено, из поля "Наименование" категории генерируется slug
        Далее, метод выполяет сохранение данных в базе.
        """

        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        """
        Вложенный класс Meta определяет наименование полей формы в разделе администрирования,
        а также принцип сортировки вывода списка категорий (по наименованию, по возрастанию)
        """

        verbose_name_plural = 'Categories'
        verbose_name = 'Category'
        ordering = ['name']

    def get_absolute_url(self):
        """
        Метод генерирует абсолютный путь для получения url через слаги.
        """

        return reverse("by_category", kwargs={"slug": self.slug})

    def count_all_post(self):
        return Post.objects.filter(category_id_id=self.pk).count()


class Post(models.Model):
    """
    Класс модели статей.
    Класс наследуется от встроенного класса Model.
    Задаются поля таблицы базы данных:
    category_id - ID категории статьи,
    user_id - ID пользователя - автора статьи,
    title - заголовок статьи
    slug - слаг статьи
    text - текст статьи
    post_status - статут статьи, выбирается из списка, задаваемого переменной CHOICES_STATUS
    status_update - дата и время последнего изменения статуса статьи
    date_create - дата и время создания статьи
    date_update - дата и встемя любого последнего изменения статьи
    """

    CHOICES_STATUS = [('Aip', 'Pending approval'), ('Apr', 'Approved'),
                      ('Del', 'Deleted'), ('Can', 'Declined'), ('Drf', 'Draft')]
    category_id = models.ForeignKey(
        CategoryPost,
        on_delete=models.CASCADE,
        verbose_name='Category')
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Header', max_length=64)
    slug = models.SlugField(
        allow_unicode=True,
        max_length=64,
        editable=False,
        unique=True)
    text = RichTextUploadingField(verbose_name='Description')
    post_status = models.CharField(
        max_length=3,
        choices=CHOICES_STATUS,
        default='Drf')
    status_update = models.DateTimeField(
        verbose_name='Status update date',
        default=datetime.datetime.today)
    date_create = models.DateTimeField(
        verbose_name='Post creation date',
        default=datetime.datetime.today)
    date_update = models.DateTimeField(
        verbose_name='Post update date',
        default=datetime.datetime.today)
    title_photo = models.ImageField(
        verbose_name='Image',
        validators=[valid_photo],
        null=True,
        blank=True,
        upload_to="post_title_photo",
    )

    @property
    def post_updated(self):
        """
        Свойство для определения, был ли обновлен пост. Если сравнивать date_update и date_create,
        получается разница  8e-06 секунд - и Django фиксирует обновление.
        В данном методе, передаваемом в шаблон, пост считается обновленным, если date_update > date_create на 10 сек
        """
        return (self.date_update - self.date_create).total_seconds() > 10

    def __str__(self):
        """
        Переопределения метода __str__.
        При вызове команды print метод выводит текст статьи, имя категории и имя автора.
        """
        return f'{self.text} ({self.category_id.name}) by {self.user_id.name}'

    def save(self, *args, **kwargs):
        """
        Переопределение метода save для генерации и записи слага названия статьи
        При вызове метода выполняется проверка наличия слага в базе данных. Если запись отсутствует,
        создается слаг, который помещается в поле salu, после чего данные сохраняются в базе данных
        """
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    class Meta:
        """
        Вложенный класс, определяет вид заголовков формы статей в разделе администрирования и
        определяет порядок сортироки при выводе перечня статей (по убыванию даты создания)
        """
        verbose_name_plural = 'Статьи'
        verbose_name = 'Статья'
        ordering = ['-date_create']

    def get_absolute_url(self):
        """
        Метод генерирует абсолютный путь для получения url через слаги.
        """
        return reverse(
            "post",
            kwargs={
                "slug": self.slug,
                "category_slug": self.category_id.name})

    def get_count_post(self):
        return Like.objects.filter(post_id_id=self.pk).count()

    def get_count_user(self):
        return Like.objects.filter(user_id_id=self.user_id.pk).count()

    def count_all_comment(self):
        return Comment.objects.filter(post_id_id=self.pk).count()

    def get_reason(self):
        return Reason.objects.filter(post_id_id=self.pk)

    def delta_update(self):

        delta = (now - self.status_update)
        if delta.days < 1:
            answer = "Less than 1 day"
        elif delta.days == 1:
            answer = f"{delta.days} 1 day ago"
        elif 2 >= delta.days < 5:
            answer = f"{delta.days} days ago"
        else:
            answer = f"{delta.days} days ago"
        return answer

# Удаляет файл фотографии если удалена запись о ней из базы
@receiver(post_delete, sender=Post)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)


class Comment(models.Model):
    """
    Класс модели комментариев.
    Класс наследуется от встроенного класса Model.
    Задаются поля таблицы базы данных:
    user_id - ID пользователя
    post_id - ID статьи
    parent_comment - 'родительский' комментарий, к которому относится данный комментарий
    (поле будет пустым, если комментируется статья, а не комментарий)
    text
    date_create - дата и время созадния статьи
    date_update - дата и время последнего изменения статьи
    """

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='replies',
        on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Comment')
    date_create = models.DateTimeField(
        verbose_name='Дата создания комментария',
        default=datetime.datetime.today)
    date_update = models.DateTimeField(
        verbose_name='Дата изменения комментария',
        default=datetime.datetime.today)
    comment_status = models.CharField(
        verbose_name='Comment status',
        max_length=3,
        null=True,
        blank=True
    )

    def __str__(self):
        """
        Переопределения метода __str__.
        При вызове команды print метод выводит текст комментария, имя автора и наименование комментируемой статьи.
        """
        return f'{self.text} by {self.user_id.name} ({self.post_id.title})'

    def get_review(self):
        return Comment.objects.filter(parent_comment_id=self.pk)

    def get_count_comment(self):
        return Like.objects.filter(comment_id_id=self.pk).count()

    def delta_update(self):
        delta = (now - self.date_create)
        if delta.days < 1:
            answer = "Less than a day ago"
        elif delta.days == 1:
            answer = f"{delta.days} 1 day ago"
        elif 2 >= delta.days < 5:
            answer = f"{delta.days} days ago"
        else:
            answer = f"{delta.days} days ago"
        return answer


class Like(models.Model):
    """
    Класс модели Лайков.
    Класс наследуется от встроенного класса Model.
    Задаются поля таблицы базы данных:
    author_user_id - ID автора статьи, получающего лайк
    user_id - ID пользователя, ставящего лайк
    post_id - ID поста, которому ставится лайк
    comment_id - ID комментарию, которому ставится лайт
    date_create - дата создания лайка
    date_update - дата последнего изменения лайка
    """

    author_user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='Author_like')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=None,
                                null=True,
                                blank=True)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, default=None,
                                null=True,
                                blank=True)
    comment_id = models.ForeignKey(
        Comment, on_delete=models.CASCADE, default=None,
        null=True,
        blank=True)
    date_create = models.DateTimeField(default=datetime.datetime.today)
    date_update = models.DateTimeField(default=datetime.datetime.today)


class Reason(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(
        Post, on_delete=models.CASCADE)
    text = models.TextField(
        verbose_name="reason for decline",
        max_length=512, blank=False)
    date_create = models.DateTimeField(
        default=datetime.datetime.today)


class Video(models.Model):
    title = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='video/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
