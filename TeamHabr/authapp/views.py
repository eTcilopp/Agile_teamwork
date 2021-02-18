from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .models import User
from .forms import UserLoginForm, UserRegisterForm, UserEditForm
from django.views.generic import UpdateView
from django.contrib import auth
from django.urls import reverse, reverse_lazy
from django.views import View
from mainapp.models import Post
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.core.mail import EmailMessage


class LoginView(LoginView):
    form = UserLoginForm
    title = 'Авторизация'

    form = UserLoginForm
    content = {
        "title": title,
        "login_form": form
    }

    def get(self, request, *args, **kwargs):
        return render(request, 'authapp/login.html', self.content)

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        redirect_to = self.request.GET.get('next')
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
            return redirect(redirect_to)


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
        return HttpResponseRedirect(reverse("main:index"))
        # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


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
            new_user = register_form.save(commit=False)
            new_user.is_active = False
            new_user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('authapp/acc_active_email.html', {
                'user': new_user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token': default_token_generator.make_token(new_user),
            })
            to_email = register_form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Для активации Вашего профиля перейдите по ссылке, отправленной Вам по электронной почте')
            # username = register_form.cleaned_data.get('username')
            # password = register_form.cleaned_data.get('password1')
            # register_form.save()
            # new_user = auth.authenticate(username=username, password=password)
            # auth.login(request, new_user)
            # return HttpResponseRedirect(reverse("main:index"))
        else:
            messages.info(request, "Регистрация невозможна.\n Введите корректные данные")
            return redirect('auth:register')


class Activate(View):

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model()._default_manager.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return HttpResponse('Благодарим Вас за подтверждение электронной почты. Вы можете авторизоваться.')
        else:
            return HttpResponse('Ссылка недействительна!')


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


# class Edit(View):
#     """
#     Класс контроллера обработки запросов на изменение данных пользователя
#
#     """
#     title = 'Редактирование'
#     form = UserEditForm
#     template_name = 'authapp/edit.html'
#     content = {
#         'title': title,
#         'form': form
#     }
#
#     def get(self, request, *args, **kwargs):
#         """
#         Функция обработки get-запросов на редактирование информации о пользователе
#         :param request - функция получает объект request, содержащий параметры запроса
#         :return: render() - функция возвращает функцию render, комбинирующую указанный шаблон
#         со славарём с передаваемыми шаблону данными;
#         """
#         return render(request, self.template_name, self.content)
#
#     def post(self, request):
#         """
#         Функция обработки post-запросов на редактиирвание данных пользователя
#         Функция определяет валидность введенных в форму данных и выполняет запись данных в базу данных.
#         :param request - фукнция получает объект request, содержажщий параментры запроса
#         :return: render() - функция возвращает функцию render, комбинирующую указанный шаблон
#         со словарем с передаваемыми шаблону данными;
#         """
#         edit_form = self.form(
#             request.POST,
#             request.FILES,
#             instance=request.user)
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('auth:edit'))
#
#         return render(request, self.template_name, self.content)


# TODO: проверить PermissionsMixin


class UserUpdate(UpdateView):
    """
    Класс контроллера обработки запросов на изменение данных пользователя

    """
    model = User
    fields = ['username', 'name', 'surname', 'email', 'age', 'aboutMe', 'avatar']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy("authapp:account")

    def get_object(self):
        return self.request.user
