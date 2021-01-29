from django.views import View
from django.shortcuts import render, get_object_or_404
from authapp.models import User
from .forms import CommentForm, PostCreationForm
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import CreateView
from django.urls import reverse, reverse_lazy
from django.db import transaction
from .models import Post, CategoryPost
from slugify import slugify


# Create your views here.


class Index(View):
    title = 'Главная'
    template_name = 'mainapp/index.html'
    categories = CategoryPost.objects.all()
    context = {
        'title': title,
        'categories': categories,
    }

    def get(self, request, slug="all", *args, **kwargs):
        """
        ТЕКСТ
        :param request - ТЕКСТ
        :return: render(request, self.template_name, self.context) - ТЕКСТ
        """

        if slug == "all":
            articles = Post.objects.filter(post_status='Apr').order_by('-date_update')
        else:
            category = get_object_or_404(CategoryPost, slug=slug)
            articles = Post.objects.filter(post_status='Apr', category_id=category).order_by('-date_update')
        self.context.update({'articles': articles})
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


class ArticleCreate(CreateView):

    model = Post
    fields = ['title', 'text', 'category_id']
    success_url = reverse_lazy("authapp:account")

    def get_context_data(self, **kwargs):
        data = super(ArticleCreate, self).get_context_data(**kwargs)

        if self.request.POST:
            form = PostCreationForm(self.request.POST)
        else:
            form = PostCreationForm
        data["postitems"] = form

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        postitems = context["postitems"]
        with transaction.atomic():
            form.instance.user_id = self.request.user
            slug = form.cleaned_data.get("title")
            form.instance.slug = slugify(slug)
            self.object = form.save()
            if postitems.is_valid():
                postitems.instance = self.object
                postitems.save()

        return super(ArticleCreate, self).form_valid(form)
