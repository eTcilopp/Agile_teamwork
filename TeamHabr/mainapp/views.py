from django.views import View
from django.shortcuts import render
from authapp.models import User
from .forms import CreateArticleForm
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views import View


# Create your views here.


class Index(View):
    title = 'Главная'
    template_name = 'mainapp/index.html'
    context = {
        'title': title,
    }

    def get(self, request, *args, **kwargs):
        """
        ТЕКСТ
        :param request - ТЕКСТ
        :return: render(request, self.template_name, self.context) - ТЕКСТ
        """
        return render(request, self.template_name, self.context)


class Design(View):
    title = 'Дизайн'
    template_name = 'mainapp/index.html'
    context = {
        'title': title,
    }

    def get(self, request, *args, **kwargs):
        """
        ТЕКСТ
        :param request - ТЕКСТ
        :return: render(request, self.template_name, self.context) - ТЕКСТ
        """
        return render(request, self.template_name, self.context)


class MobileDevelopment(View):
    title = 'Мобильная разработка'
    template_name = 'mainapp/index.html'
    context = {
        'title': title,
    }

    def get(self, request, *args, **kwargs):
        """
        ТЕКСТ
        :param request - ТЕКСТ
        :return: render(request, self.template_name, self.context) - ТЕКСТ
        """
        return render(request, self.template_name, self.context)


class WebDevelopment(View):
    title = 'Веб разработка'
    template_name = 'mainapp/index.html'
    context = {
        'title': title,
    }

    def get(self, request, *args, **kwargs):
        """
        ТЕКСТ
        :param request - ТЕКСТ
        :return: render(request, self.template_name, self.context) - ТЕКСТ
        """
        return render(request, self.template_name, self.context)


class Marketing(View):
    title = 'Маркетинг'
    template_name = 'mainapp/index.html'
    context = {
        'title': title,
    }

    def get(self, request, *args, **kwargs):
        """
        ТЕКСТ
        :param request - ТЕКСТ
        :return: render(request, self.template_name, self.context) - ТЕКСТ
        """
        return render(request, self.template_name, self.context)


class HelpPage(View):
    title = 'Помощь'
    template_name = 'mainapp/index.html'
    context = {
        'title': title,
    }

    def get(self, request, *args, **kwargs):
        """
        ТЕКСТ
        :param request - ТЕКСТ
        :return: render(request, self.template_name, self.context) - ТЕКСТ
        """
        return render(request, self.template_name, self.context)


# @login_required
# def account(request):
#     """
#     Контроллер личного кабинета. Для входа в личный кабинет требуется аутентификация.
#     :param request -
#     :return: render(request, 'mainapp/account.html', context)
#     """
#
#     title = 'Личный кабинет'
#     context = {
#         'title': title
#     }
#     first_name = request.user.name
#     last_name = request.user.surname
#     html = f'<h1>Личный кабинет пользователя: {first_name} {last_name}</h1>'
#     return HttpResponse(html)


class Account(View):
    title = 'Личный кабинет пользователя'
    template_name = 'mainapp/account.html'
    context = {
        'title': title
    }

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)


class ArticleCreate(View):
    title = 'Создание новой статьи'
    template_name = 'mainapp/article-create.html'



    def post(self, request):
        form = CreateArticleForm(request.POST)
        context = {
            'title': self.title,
            'form': form,
        }
        if form.is_valid():
            #form.save()
            return redirect('mainapp:account')
        return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        form = CreateArticleForm()
        context = {
            'title': self.title,
            'form': form,
        }
        return render(request, self.template_name, context)
