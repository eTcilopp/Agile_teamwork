from django.views import View
from django.shortcuts import render
from authapp.models import User
from .forms import CommentForm, PostCreationForm
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


class ArticleCreate(View):
    title = 'Создание новой статьи'
    template_name = 'mainapp/article-create.html'

    def post(self, request):
        form = PostCreationForm(request.POST)
        context = {
            'title': self.title,
            'form': form,
        }
        if form.is_valid():
            form.save()
            return redirect('authapp:account')
        return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        form = PostCreationForm()
        context = {
            'title': self.title,
            'form': form,
        }
        return render(request, self.template_name, context)
