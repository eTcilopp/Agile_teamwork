from django.contrib import admin
from .models import Post, Comment, CategoryPost, Like


class PostAdmin(admin.ModelAdmin):
    pass


class CategoryPostAdmin(admin.ModelAdmin):
    pass


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(CategoryPost, CategoryPostAdmin)
admin.site.register(Like)
