from django.views import View
from django.shortcuts import render, get_object_or_404
from authapp.models import User
from .forms import CommentForm, PostCreationForm
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import CreateView, ListView
from django.views.generic.detail import DetailView
from django.urls import reverse, reverse_lazy
from django.db import transaction
from .models import Post, CategoryPost
from slugify import slugify


# Create your views here.


class Index(ListView):
    paginate_by = 4
    model = Post

    def get_queryset(self, *args, **kwargs):
        queryset = self.model.objects.filter(
                post_status='Apr')
        if self.kwargs.get('slug'):
            queryset = self.model.objects.filter(
                category_id__slug=self.kwargs['slug'], post_status='Apr')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        context['categories'] = CategoryPost.objects.all()
        return context


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


class PostRead(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostRead, self).get_context_data(**kwargs)
        context["title"] = "Статья"
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Post, slug=self.kwargs.get('slug'))

