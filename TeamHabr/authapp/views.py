from django.shortcuts import HttpResponseRedirect, render
from .models import User
from .forms import UserLoginForm, UserRegisterForm
from django.contrib import auth
from django.urls import reverse


# Create your views here.

def login(request):
    title = 'Авторизация'

    login_form = UserLoginForm()

    if request.method == "POST" and login_form.is_valid():
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse("index"))

    content = {
        "title": title,
        "login_form": login_form
    }
    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    title = "регистрация"

    if request.method == "POST":
        register_form = UserRegisterForm(request.POST)

        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse("auth:login"))
    else:
        register_form = UserRegisterForm()

    content = {"title": title, "register_form": register_form}
    return render(request, "authapp/register.html", content)
