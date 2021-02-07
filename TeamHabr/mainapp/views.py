from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .forms import PostCreationForm, CommentForm
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.db import transaction
from .models import Post, CategoryPost, Comment, Like
from slugify import slugify
import re
import datetime


def likes(request, pk, type_likes):
    """
    Функция создания лайков
    :param request:
    :param pk:
    :param type_likes:
    :return:
    """
    field_id = f"{type_likes}_id_id"
    author = request.user
    obj, created = Like.objects.update_or_create(**{field_id: pk}, author_user_id_id=author.pk)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class Index(ListView):
    """
    Класс контроллера обрабоки запросов на просмотр главной станицы.
    Класс наследует от встроенного класса ListView
    Задается связанная модель
    Задается количество статей, выводимых на одном экране одновременно (пагинация)
    """
    model = Post
    paginate_by = 4

    def get_queryset(self, *args, **kwargs):
        """
        Функция получения набора данных со статьями из базы данных. Выдираются только статьи со статусом 'Утверждено'
        В случае, если запросе присутствуте поле 'slug', фильтрация выполняется и по полю slug категории
        Функция возвращает queryset, используемой родительским классом ListView
        """
        queryset = self.model.objects.filter(
            post_status='Apr')
        if self.kwargs.get('slug'):
            queryset = self.model.objects.filter(
                category_id__slug=self.kwargs['slug'], post_status='Apr')
        return queryset

    def get_context_data(self, **kwargs):
        """
        Переопределение встроенной функция получения информации из базы данных,
        передаваемой шаблону для формирования главной старицы.
        В словарь context добавляются значения заголовка и списка категорий для формирования меню.
        """
        context = super().get_context_data(**kwargs)
        if self.kwargs.get('slug'):
            category = CategoryPost.objects.filter(slug=self.kwargs['slug'])
            context['title'] = category[0].name
        else:
            context['title'] = 'Главная'
        context['categories'] = CategoryPost.objects.all()
        return context


class ArticleCreate(CreateView):
    """
    Класс контроллера обрабоки запросов на создание новой статьи.
    Класс наследуется от встроенного класса CreateView
    Задается связанная модель - Post
    Определяются отображаемые поляЖ 'title', 'text', 'category_id'
    Задается url для перехода в случае успешного создания статьи
    """

    model = Post
    category_post_model = CategoryPost
    fields = ['title', 'text', 'category_id']
    success_url = reverse_lazy("authapp:account")

    def get_initial(self):
        """
        Функция задает исходные параметры полей формы создания статьи
        :return: функуия возвращает словарь initial, содержащий исходные (присутствующие по умолчанию) параметры
        """
        initial = super(ArticleCreate, self).get_initial()
        # опделеляем url страницы, с которой осуществлен переход
        source_page = self.request.META["HTTP_REFERER"]
        # с помощью регулярного выражения определен слаг страницы, с которой выполнен переход
        result = re.search('.*/(.*)/', source_page).group(1)
        # выполняется запрос в базу данных - по слагу определяется id категории из модели CategoryPost
        category_id = self.category_post_model.objects.filter(
            slug=result).values_list('id', flat=True).first()
        # в случае, если категория найдена, ее значение добавляется в словарь itinial для передачи в форму
        if category_id:
            initial['category_id'] = category_id
        return initial

    def get_context_data(self, **kwargs):
        """
        Переопределение встроенного метода get_context_data
        Добавляется проверка: в случае получения запроса методом POST, создается экземпляр класса PostCreationForm
        с параметром POST, и с заполненными полями.
        если запрос получен другим методом (очевидно, get),
        создается экземпляр класса PostCreationForm с пустыми полями.
        Далее, в словарь data добавляется экземпряр класса PostCreationForm и обновленный словарь возвращается шаблону.
        """
        data = super(ArticleCreate, self).get_context_data(**kwargs)

        if self.request.POST:
            form = PostCreationForm(self.request.POST)
        else:
            form = PostCreationForm
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
            form.instance.user_id = self.request.user
            slug = form.cleaned_data.get("title")
            form.instance.slug = slugify(slug)
            self.object = form.save()
            if postitems.is_valid():
                postitems.instance = self.object
                postitems.save()

        return super(ArticleCreate, self).form_valid(form)

class ArticleUpdate(UpdateView):

    model = Post
    fields = ['title', 'text', 'category_id', 'date_update', 'post_status']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy("authapp:account")


    def get_initial(self):
        """
        Функция задает исходные параметры полей формы создания статьи
        :return: функуия возвращает словарь initial, содержащий исходные (присутствующие по умолчанию) параметры
        """
        initial = super(ArticleUpdate, self).get_initial()
        initial['date_update'] = datetime.datetime.today
        initial['post_status'] = 'Drf'
        return initial
    #TODO: спрятать date_update и post_status - думаю, надо переопределить форму и задать в ней.
    #TODO - сделать возврат на ту страницу, откуда пришел запрос на редактирование
    #TODO - сделать, чтобы редактировать статью можно было со страницы статьи
    #TODO- переход на страницу статьи можно делать, кликнув по заголовку статьи
    #TODO - авить дату обновления к дате создания


class PostRead(DetailView):
    """
    Класс контроллера обрабоки запросов на просмотр индивидуальной статьи.
    Класс наследуется от встроенного класса DetailView
    Задается связанная модель - Post
    """
    model = Post
    form = CommentForm

    def get_success_url(self):
        return reverse_lazy('main:post', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        """
        В словарь контекста data добавляется заголовок страницы, коментарии, количество коментариев
        """
        context = super(PostRead, self).get_context_data(**kwargs)
        context["title"] = "Статья"
        context["comments"] = Comment.objects.filter(post_id=self.get_object().id, parent_comment=None)
        context['form'] = self.form()
        return context

    def form_valid(self, form):
        """
        Метод выполняет проверку правильности заполнения формы данными,
        осуществляет дозаполнение полeй юзера и id статьи,
        сохраняет данные в базе данных безопасным для даных образом (по принципу 'все или ничего')
        """
        form.instance.post_id = self.object
        form.instance.user_id = self.request.user
        if self.request.POST.get("parent", None):
            form.instance.parent_comment_id = int(self.request.POST.get("parent"))
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """
        Метод выполняется при не прохождении проверки правильности заполнения формы данными
        """
        return self.render_to_response(self.get_context_data(form=form))

    def get_object(self, queryset=None):
        """
        Функция возвращает объект со статьей и базы данных, найденный по полю slug
        """
        return get_object_or_404(Post, slug=self.kwargs.get('slug'))

    def post(self, *args, **kwargs):
        """
        Метод срабатывает при отправке данных из формы коментариев
        """
        self.object = self.get_object()
        form = self.form(self.request.POST)
        print(form)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class HelpPage(View):
    """
    Класс контроллера обрабоки запросов на просмотр станицы помощи.
    Класс наследуется от встроенного класса View
    Для формирования словаря context задается заголовок, имя шаблона, контекст.
    """
    title = 'Помощь'
    template_name = 'mainapp/index.html'
    context = {
        'title': title,
    }

    def get(self, request, *args, **kwargs):
        """
        Метод обработки заросов get для просмотра страницы помощи.
        Метод возвращает функцию render с объектом request, содержащим зарпос, имя шаблона
        и словарь с передаваемыми шаблону данными.
        """
        return render(request, self.template_name, self.context)
