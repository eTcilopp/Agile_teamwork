from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import datetime
from slugify import slugify

from authapp.models import User
from mainapp.models import Post, CategoryPost, Reason
from mainapp.forms import ReasonCreateForm
from adminapp.forms import CategoryCreationForm


class ReasonCreate(CreateView):
    model = Reason
    fields = ['text']
    form = ReasonCreateForm
    template_name = 'adminapp/create.html'

    def get_success_url(self):
        """
        url для перехода в случае успешного создания статьи
        """

        return reverse_lazy('admin:post_list')

    def get_context_data(self, **kwargs):
        """
        В словарь контекста data добавляется заголовок страницы
        """

        context = super(ReasonCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            print(self.request)
            form = ReasonCreateForm(self.request.POST)
        else:
            form = ReasonCreateForm
        context["title"] = "Создание причины отказа"
        context["postitems"] = form
        return context

    def form_valid(self, form, **kwargs):
        """
        Метод выполняет проверку правильности заполнения формы данными,
        осуществляет дозаполнение поля сгенерируемым автоматически слагом,
        сохраняет данные в базе данных безопасным для даных образом (по принципу 'все или ничего')
        """

        context = self.get_context_data()
        postitems = context["postitems"]
        with transaction.atomic():
            post = Post.objects.get(slug=self.kwargs['slug'])
            form.instance.post_id_id = post.pk
            form.instance.user_id_id = self.request.user.pk
            self.object = form.save()
            if postitems.is_valid():
                postitems.instance = self.object
                postitems.save()
                Post.objects.filter(
                    slug=self.kwargs['slug']).update(
                    post_status=self.kwargs['status'],
                    status_update=datetime.datetime.now())

                current_site = get_current_site(self.request)
                mail_subject = 'Отклонение вашей статьи.'
                message = render_to_string('adminapp/cancel_email.html', {
                    'domain': current_site.domain,
                    'post': post,
                    'moder': self.request.user.username
                })
                to_email = post.user_id.email
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
        return super(ReasonCreate, self).form_valid(form)


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список пользователей'
        context['categories'] = CategoryPost.objects.all()
        return context


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

    def get_queryset(self, *args, **kwargs):
        """
        Функция получения набора данных со статьями из базы данных. Выдираются только статьи со статусом 'Утверждено'
        В случае, если запросе присутствуте поле 'slug', фильтрация выполняется и по полю slug категории
        Функция возвращает queryset, используемой родительским классом ListView
        """

        if self.kwargs.get('status'):
            # print(self.kwargs['status'])
            queryset = self.model.objects.filter(post_status=self.kwargs['status'])
        else:
            queryset = self.model.objects.exclude(
                post_status='Drf').order_by('post_status')
        return queryset

    def get_context_data(self, **kwargs):
        """
        Переопределение встроенной функция получения информации из базы данных,
        передаваемой шаблону для формирования главной старицы.
        В словарь context добавляются значения заголовка и списка категорий для формирования меню.
        """

        context = super().get_context_data(**kwargs)
        context['title'] = 'Список статей'
        context['categories'] = CategoryPost.objects.all()
        context['Aip'] = Post.objects.filter(post_status='Aip').count
        context['Apr'] = Post.objects.filter(post_status='Apr').count
        context['Can'] = Post.objects.filter(post_status='Can').count
        context['Del'] = Post.objects.filter(post_status='Del').count
        return context

    def post(self, request):
        print(self.request.POST['status_list'])
        print(self.request)


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

    def get_context_data(self, **kwargs):
        context = super(AdminCategoryList, self).get_context_data(**kwargs)
        context['title'] = 'Список категорий'
        context['categories'] = CategoryPost.objects.all()
        return context


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

        context = super(AdminCreateCategory, self).get_context_data(**kwargs)
        if self.request.POST:
            form = CategoryCreationForm(self.request.POST)
        else:
            form = CategoryCreationForm
        context["title"] = "Создание новой категории"
        context["postitems"] = form
        context['categories'] = CategoryPost.objects.all()
        return context

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


def change_status_post(request, slug, status):
    if status == "Can":
        return redirect('admin:create_reason', slug=slug, status=status)
    else:
        if status == "Apr":
            post = Post.objects.get(slug=slug)
            if Reason.objects.filter(post_id_id=post.pk).exists():
                Reason.objects.filter(post_id_id=post.pk).delete()
        Post.objects.filter(slug=slug).update(post_status=status, status_update=datetime.datetime.now())
        post_to_email = Post.objects.get(slug=slug)
        current_site = get_current_site(request)
        mail_subject = 'Изменение статуса вашей статьи.'
        message = render_to_string('adminapp/email_change_status_message.html', {
            'domain': current_site.domain,
            'post': post_to_email
        })
        to_email = post_to_email.user_id.email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@user_passes_test(lambda u: u.is_superuser)
def create_moder(request, pk):
    """
    Функция назначает пользователя в группу Moder
    :param request:
    :param pk: ID_USER
    :return: Обратно на страницу админки
    """

    my_group, created = Group.objects.get_or_create(name='Moder')

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
