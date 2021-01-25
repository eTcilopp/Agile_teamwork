from django.shortcuts import render
# TODO - удалить после того, как будет готов шаблон Личного кабинета
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from authapp.models import User


# Create your views here.


def index(request):
    """
    ТЕКСТ
    :param request - ТЕКСТ
    :return: render(request, 'mainapp/index.html', context) - ТЕКСТ
    """
    title = 'Главная'
    users = User.objects.all()
    print(users)
    context = {
        'title': title, 'users': users,
    }
    return render(request, 'mainapp/index.html', context)


def design(request):
    """
    ТЕКСТ
    :param request - ТЕКСТ
    :return: render(request, 'mainapp/index.html', context) - ТЕКСТ
    """
    title = 'Дизайн'
    context = {
        'title': title,
    }
    return render(request, 'mainapp/index.html', context)


def mobile_development(request):
    """
    ТЕКСТ
    :param request - ТЕКСТ
    :return: render(request, 'mainapp/index.html', context) - ТЕКСТ
    """
    title = 'Мобильная разработка'
    context = {
        'title': title,
    }
    return render(request, 'mainapp/index.html', context)


def web_development(request):
    """
    ТЕКСТ
    :param request - ТЕКСТ
    :return: render(request, 'mainapp/index.html', context) - ТЕКСТ
    """
    title = 'Веб разработка'
    context = {
        'title': title,
    }
    return render(request, 'mainapp/index.html', context)


def marketing(request):
    title = 'Маркетинг'
    context = {
        'title': title,
    }
    return render(request, 'mainapp/index.html', context)


def help_page(request):
    """
    ТЕКСТ
    :param request - ТЕКСТ
    :return: render(request, 'mainapp/index.html', context) - ТЕКСТ
    """
    title = 'Помощь'
    context = {
        'title': title,
    }
    return render(request, 'mainapp/index.html', context)


@login_required
def account(request):
    """
    Контроллер личного кабинета. Для входа в личный кабинет требуется аутентификация.
    :param request -
    :return: render(request, 'mainapp/account.html', context)
    """

    title = 'Личный кабинет'
    context = {
        'title': title
    }
    first_name = request.user.name
    last_name = request.user.surname
    html = f'<h1>Личный кабинет пользователя: {first_name} {last_name}</h1>'
    return HttpResponse(html)
