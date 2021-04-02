from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import UpdateView
from django.contrib import auth
from django.urls import reverse, reverse_lazy
from django.views import View
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.core.mail import EmailMessage
from django.views.generic.detail import DetailView

from .models import User
from mainapp.models import Post, CategoryPost
from .forms import UserRegisterForm


class LoginView(LoginView):

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
            return redirect(redirect_to+"#valid")


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


class Register(View):
    """
    Класс контроллера обрабоки запросов на регистрацию нового пользователя.
    """

    title = 'Регистрация'
    form = UserRegisterForm
    template_name = 'authapp/register.html'
    content = {
        "title": title,
        "register_form": form,
        'categories': CategoryPost.objects.all(),
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
            new_user.avatar = 'users_avatars/00_default_avatar.png'
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
            template_name = 'authapp/service_messages.html'
            service_message = 'Для активации Вашего профиля перейдите по ссылке, отправленной Вам по электронной почте.'
            content = {"service_message": service_message}
            return render(request, template_name, content)
        else:
            self.content["register_form"] = register_form
            return render(request, self.template_name, self.content)


class Activate(View):
    title = 'Страница подтверждения'
    template_name = 'authapp/service_messages.html'
    service_message = 'Благодарим Вас за подтверждение электронной почты. Вы можете авторизоваться.'
    context = {
        'title': title,
        'service_message': service_message,
        'categories': CategoryPost.objects.all(),
    }

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model()._default_manager.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(
                user, token):
            user.is_active = True
            user.save()
            self.context['login_allowed'] = True
            #TODO: при авторизации по ссылке из письма нужно уходить с этой страницы. Спросить МИхаила.
        else:
            self.context['service_message'] = 'Ссылка устарела или недействительна.'
        return render(request, self.template_name, self.context)


class Account(DetailView):
    """
    Класс контроллера обрабоки запросов на просмотр личного кабинета пользователя.
    """

    title = 'Личный кабинет пользователя'
    template_name = 'authapp/account.html'
    context = {
        'title': title,
        'categories': CategoryPost.objects.all(),
    }

    def get(self, request, *args, **kwargs):
        """
        Функция обработки get-запросов на просмотр личного кабинета пользователя.
        :param request - фукнция получает объект request, содержажщий параментры запроса
        :return: render() - функция возвращает функцию render, комбинирующую указанный шаблон
        со словарем с передаваемыми шаблону данными;
        """
        if self.kwargs.get('status'):
            articles = Post.objects.filter(
                user_id=self.request.user.id, post_status=self.kwargs['status'])
        else:
            articles = Post.objects.filter(
                user_id=self.request.user.id).exclude(
                post_status='Del')

        self.context['Aip'] = Post.objects.filter(user_id=self.request.user.id, post_status='Aip').count
        self.context['Apr'] = Post.objects.filter(user_id=self.request.user.id, post_status='Apr').count
        self.context['Can'] = Post.objects.filter(user_id=self.request.user.id, post_status='Can').count
        self.context['Drf'] = Post.objects.filter(user_id=self.request.user.id, post_status='Drf').count
        self.context['articles'] = articles
        return render(request, self.template_name, self.context)
# TODO: проверить PermissionsMixin


class UserUpdate(UpdateView):
    """
    Класс контроллера обработки запросов на изменение данных пользователя
    """

    model = User
    fields = [
        'username', 'email',
        'name',
        'surname',
        'age',
        'avatar',
        'aboutMe',
        ]
    template_name_suffix = '_update_form'
    success_url = reverse_lazy("authapp:account")

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(UserUpdate, self).get_context_data(**kwargs)
        context['title'] = 'Редактирование данных пользователя'
        context['categories'] = CategoryPost.objects.all()
        return context
