from django.shortcuts import render
from django.views.generic import CreateView, ListView
from authapp.models import User
from mainapp.models import Post, CategoryPost
from adminapp.forms import CategoryCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.db import transaction
from slugify import slugify
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group


@user_passes_test(lambda u: u.is_superuser)
def create_moder(request, pk):
    """
    Функция назначает пользователя в группу Moder
    :param request:
    :param pk: ID_USER
    :return: Обратно на страницу админки
    """
    my_group = Group.objects.get(name='Moder')
    my_group.user_set.add(pk)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@user_passes_test(lambda u: u.is_superuser)
def delete_moder(request, pk):
    """
        Функция удаляет пользователя из группы Moder
        :param request:
        :param pk: ID_USER
        :return: Обратно на страницу админки
        """
    my_group = Group.objects.get(name='Moder')
    my_group.user_set.remove(pk)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class AdminUserList(LoginRequiredMixin, ListView):
    """
        Класс контроллера обрабоки запросов на просмотр станицы
        со списком пользователей в интерфейсе админитстратора.
        Класс наследует от встроенного класса ListView
        Задается связанная модель
        Задается количество пользователей, выводимых на одном экране одновременно (пагинация)
        """
    template_name = "adminapp/user_list.html"
    model = User
    paginate_by = 10


class AdminPostList(LoginRequiredMixin, ListView):
    """
        Класс контроллера обрабоки запросов на просмотр станицы
        со списком статей в интерфейсе админитстратора.
        Класс наследует от встроенного класса ListView
        Задается связанная модель
        Задается количество статей, выводимых на одном экране одновременно (пагинация)
        """
    template_name = "adminapp/post_list.html"
    model = Post
    paginate_by = 10


class AdminCategoryList(LoginRequiredMixin, ListView):
    """
        Класс контроллера обрабоки запросов на просмотр станицы
        со списком категорий в интерфейсе админитстратора.
        Класс наследует от встроенного класса ListView
        Задается связанная модель
        Задается количество категорий, выводимых на одном экране одновременно (пагинация)
        """
    template_name = "adminapp/category_list.html"
    model = CategoryPost

    paginate_by = 10


class AdminCreateCategory(CreateView):
    """
            Класс контроллера обрабоки запросов
            на создание категории в интерфейсе админитстратора.
            Класс наследует от встроенного класса CreateView
            Задается связанная модель - CategoryPost
            Определяются отображаемые поляЖ 'name', 'description'
            Задается url для перехода в случае успешного создания статьи
            """
    model = CategoryPost
    fields = ['name', 'description']
    form = CategoryCreationForm

    template_name = "adminapp/create.html"

    def get_success_url(self):
        """
        url для перехода в случае успешного создания статьи
        """
        return reverse_lazy('admin:category_list')

    def get_context_data(self, **kwargs):
        """
        В словарь контекста data добавляется заголовок страницы
        """
        data = super(AdminCreateCategory, self).get_context_data(**kwargs)

        if self.request.POST:
            form = CategoryCreationForm(self.request.POST)
        else:
            form = CategoryCreationForm
        data["postitems"] = form

        return data

    def form_valid(self, form):
        """
        Метод выполняет проверку правильности заполнения формы данными,
        осуществляет дозаполнение поля сгенерируемым автоматически слагом,
        сохраняет данные в базе данных безопасным для даных образом (по принципу 'все или ничего')
        """
        context = self.get_context_data()
        postitems = context["postitems"]
        with transaction.atomic():
            slug = form.cleaned_data.get("name")
            form.instance.slug = slugify(slug)
            self.object = form.save()
            if postitems.is_valid():
                postitems.instance = self.object
                postitems.save()

        return super(AdminCreateCategory, self).form_valid(form)
