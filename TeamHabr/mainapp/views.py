from django.shortcuts import render

# Create your views here.


def index(request):
    """
    ТЕКСТ
    :param request - ТЕКСТ
    :return: render(request, 'mainapp/index.html', context) - ТЕКСТ
    """
    title = 'Главная'
    context = {
        'title': title,
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
