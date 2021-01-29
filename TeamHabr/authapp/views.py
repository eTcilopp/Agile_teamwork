from django.shortcuts import HttpResponseRedirect, render
from .models import User
from .forms import UserLoginForm, UserRegisterForm
from django.contrib import auth
from django.urls import reverse
from django.views import View
from mainapp.models import Post


# Create your views here.


class Login(View):
    title = 'Авторизация'
    form = UserLoginForm
    template_name = 'authapp/login.html'
    content = {
        "title": title,
        "login_form": form
    }

    def get(self, request, *args, **kwargs):
        """
        ТЕКСТ
        :param request - ТЕКСТ
        :return: render(request, self.template_name, self.content) - ТЕКСТ
        """
        return render(request, self.template_name, self.content)

    def post(self, request, *args, **kwargs):
        """
        ТЕКСТ
        :param request - ТЕКСТ
        :return: render(request, self.template_name, self.content) - ТЕКСТ
        """
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse("main:index"))
        return render(request, self.template_name, self.content)


class Logout(View):
    template_name = 'mainapp/index.html'

    def get(self, request, *args, **kwargs):
        """
        ТЕКСТ
        :param request - ТЕКСТ
        :return: render(request, self.template_name) - ТЕКСТ
        """
        auth.logout(request)
        return render(request, self.template_name)


class Register(View):
    title = 'Регистрация'
    form = UserRegisterForm
    template_name = 'authapp/register.html'
    content = {
        "title": title,
        "register_form": form
    }

    def get(self, request, *args, **kwargs):
        """
        ТЕКСТ
        :param request - ТЕКСТ
        :return: render(request, self.template_name, self.content) - ТЕКСТ
        """
        return render(request, self.template_name, self.content)

    def post(self, request):
        """
        ТЕКСТ
        :param request - ТЕКСТ
        :return: render(request, self.template_name, self.content) - ТЕКСТ
        """
        register_form = self.form(request.POST)
        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse("auth:login"))

        return render(request, self.template_name, self.content)


class Account(View):
    title = 'Личный кабинет пользователя'
    template_name = 'authapp/account.html'

    context = {
        'title': title
    }

    def get(self, request, *args, **kwargs):
        articles = Post.objects.filter(user_id=self.request.user.id).exclude(post_status='Del')
        self.context = {
            'articles': articles
        }
        return render(request, self.template_name, self.context)
