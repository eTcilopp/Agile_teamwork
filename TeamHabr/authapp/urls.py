from django.contrib import admin
from django.urls import path, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
import authapp.views as authapp
from django.conf import settings
from django.conf.urls.static import static

app_name = 'authapp'

"""
Ссылки на элементы приложения authapp
login - Создание процедуры Авторизации 
logout - Процедура разлогинивания
register - Создание процедуры Регистрации
account - Вывод страницы личного кабинета
"""

urlpatterns = [
    path(
        'login/',
        authapp.LoginView.as_view(), name='login'),
    path(
        'logout/',
        authapp.Logout.as_view(),
        name='logout'),
    path(
        'register/',
        authapp.Register.as_view(),
        name='register'),
    path('activate/<uidb64>/<token>/',
         authapp.Activate.as_view(),
         name='activate'),
    path(
        'account/',
        login_required(
            authapp.Account.as_view()),
        name='account'),
    path(
        'account/<str:status>/',
        login_required(
            authapp.Account.as_view()),
        name='account_post_status'),
    # path(
    #     'edit/',
    #     authapp.Edit.as_view(),
    #     name='edit', ),
    path('update/',
         authapp.UserUpdate.as_view(),
         name='edit'),
    path('account/password_reset/', auth_views.PasswordResetView.as_view(
        template_name="authapp/reset_password.html",
        email_template_name="authapp/password_reset_html_email.html",
        success_url=reverse_lazy('authapp:password_reset_done')),
         name='reset_password'),
    path('account/password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name="authapp/password_reset_sent.html"
         ),
         name='password_reset_done'),
    path('account/reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="authapp/password_reset_form.html",
             success_url=reverse_lazy("authapp:password_reset_complete")
         ),
         name='password_reset_confirm'),
    path('account/reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="authapp/password_reset_done.html"
         ),
         name='password_reset_complete'),
    path('account/password_change/',
         auth_views.PasswordChangeView.as_view(
             template_name="authapp/password_change_form.html",
             success_url=reverse_lazy("authapp:password_change_done")
         ),
         name='password_change'),
    path('account/password_change/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="authapp/password_change_done.html"
         ),
         name='password_change_done'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
