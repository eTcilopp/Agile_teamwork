from django.contrib import admin
from .models import Post, Comment, CategoryPost, Like

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(CategoryPost)
admin.site.register(Like)
