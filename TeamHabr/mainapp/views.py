from django.shortcuts import render

# Create your views here.


def index(request):
    title = 'Главная'
    context = {
        'title': title,
    }
    return render(request, 'mainapp/index.html', context)


def design(request):
    title = 'Дизайн'
    context = {
        'title': title,
    }
    return render(request, 'mainapp/index.html', context)


def mobile_development(request):
    title = 'Мобильная разработка'
    context = {
        'title': title,
    }
    return render(request, 'mainapp/index.html', context)


def web_development(request):
    title = 'Веб разработка'
    context = {
        'title': title,
    }
    return render(request, 'mainapp/index.html', context)


def help_page(request):
    title = 'Помощь'
    context = {
        'title': title,
    }
    return render(request, 'mainapp/index.html', context)
