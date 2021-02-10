from django.shortcuts import HttpResponseRedirect, render
from .models import User
from .forms import UserLoginForm, UserRegisterForm, UserEditForm
from django.views.generic import UpdateView
from django.contrib import auth
from django.urls import reverse, reverse_lazy
from django.views import View
from mainapp.models import Post
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib import messages


class LoginView(LoginView):
    form = UserLoginForm
    title = 'Авторизация'

    form = UserLoginForm
    content = {
        "title": title,
        "login_form": form
    }

    def get(self, request, *args, **kwargs):
        global redirect_to
        redirect_to = self.request.GET.get('next')

        # print(redirect_to)
        return render(request, 'authapp/login.html', self.content)

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        # print(redirect_to)
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            if redirect_to is None:
                return redirect('/')
            else:
                return redirect(redirect_to)
        else:
            messages.info(
                request,
                "Вход невозможен.\n Введите корректные логин/пароль")
            return redirect('auth:login')

# class Login(View):
#     """
#     Класс контроллера обрабоки запросов на авторизацию пользователя.
#     """
#     title = 'Авторизация'
#     form = UserLoginForm
#     template_name = 'authapp/login.html'
#     content = {
#         "title": title,
#         "login_form": form
#     }
#
#     def get(self, request, *args, **kwargs):
#         """
#         Функция обработки get-запросов на авторизацию пользователя.
#         :param request - фукнция получает объект request, содержажщий параментры запроса
#         :return: функция возвращает функцию render, комбинирующую указанный шаблон со словарем с передаваемыми данными;
#         """
#         return render(request, self.template_name, self.content)
#
#     def post(self, request, *args, **kwargs):
#         """
#         Функция обработки post-запросов на авторизацию пользователя.
#         Функция получает из запроса параметры username и password, после чего определяет,
#         существует ли учетная запись пользователя в базе данных и
#         не является и учетная запись деактивированной.
#         :param request - фукнция получает объект request, содержажщий параментры запроса
#         :return: функция возвращает функцию render, комбинирующую указанный шаблон
#         со словарем с передаваемыми шаблону данными;
#         """
#         username = request.POST["username"]
#         password = request.POST["password"]
#         user = auth.authenticate(username=username, password=password)
#         if user and user.is_active:
#             auth.login(request, user)
#             return HttpResponseRedirect(reverse("main:index"))
#         return render(request, self.template_name, self.content)


class Logout(View):
    """
    Класс контроллера обрабоки запросов на выход из системы авторихованного пользователя.
    """

    def get(self, request, *args, **kwargs):
        """
        Функция обработки get-запросов на выход из системы авторихованного пользователя.
        :param request - фукнция получает объект request, содержажщий параментры запроса;
        :return: функция возвращает функцию render, комбинирующую указанный шаблон со словарем
        с передаваемыми шаблону данными;
        """
        auth.logout(request)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class Register(View):
    """
    Класс контроллера обрабоки запросов на регистрацию нового пользователя.
    """
    title = 'Регистрация'
    form = UserRegisterForm
    template_name = 'authapp/register.html'
    content = {
        "title": title,
        "register_form": form
    }

    def get(self, request, *args, **kwargs):
        """
        Функция обработки get-запросов на на регистрацию нового пользователя.
        :param request - фукнция получает объект request, содержажщий параментры запроса;
        :return: функция возвращает функцию render, комбинирующую указанный шаблон со словарем
        с передаваемыми шаблону данными;
        """
        return render(request, self.template_name, self.content)

    def post(self, request):
        """
        Функция обработки post-запросов на авторизацию пользователя.
        Функция определяет валидность введенных в форму данных и выполняет запись данных в базу данных.
        :param request - фукнция получает объект request, содержажщий параментры запроса
        :return: render() - функция возвращает функцию render, комбинирующую указанный шаблон
        со словарем с передаваемыми шаблону данными;
        """
        register_form = self.form(request.POST)
        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse("auth:login"))

        return render(request, self.template_name, self.content)


class Account(View):
    """
    Класс контроллера обрабоки запросов на просмотр личного кабинета пользователя.
    """
    title = 'Личный кабинет пользователя'
    template_name = 'authapp/account.html'

    context = {
        'title': title
    }

    def get(self, request, *args, **kwargs):
        """
        Функция обработки get-запросов на просмотр личного кабинета пользователя.
        :param request - фукнция получает объект request, содержажщий параментры запроса
        :return: render() - функция возвращает функцию render, комбинирующую указанный шаблон
        со словарем с передаваемыми шаблону данными;
        """
        articles = Post.objects.filter(
            user_id=self.request.user.id).exclude(
            post_status='Del')
        self.context = {
            'articles': articles
        }
        return render(request, self.template_name, self.context)


class Edit(View):
    """
    Класс контроллера обработки запросов на изменение данных пользователя

    """
    title = 'Редактирование'
    form = UserEditForm
    template_name = 'authapp/edit.html'
    content = {
        'title': title,
        'edit_form': form
    }

    def get(self, request, *args, **kwargs):
        """
        Функция обработки get-запросов на редактирование информации о пользователе
        :param request - функция получает объект request, содержащий параметры запроса
        :return: render() - функция возвращает функцию render, комбинирующую указанный шаблон
        со славарём с передаваемыми шаблону данными;
        """
        return render(request, self.template_name, self.content)

    def post(self, request):
        """
        Функция обработки post-запросов на редактиирвание данных пользователя
        Функция определяет валидность введенных в форму данных и выполняет запись данных в базу данных.
        :param request - фукнция получает объект request, содержажщий параментры запроса
        :return: render() - функция возвращает функцию render, комбинирующую указанный шаблон
        со словарем с передаваемыми шаблону данными;
        """
        edit_form = self.form(
            request.POST,
            request.FILES,
            instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))

        return render(request, self.template_name, self.content)

# TODO: проверить PermissionsMixin


class UserUpdate(UpdateView):
    """
    Класс контроллера обработки запросов на изменение данных пользователя

    """
    model = User
    fields = ['username', 'name', 'surname', 'email']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy("authapp:account")

    def get_object(self):
        return self.request.user
