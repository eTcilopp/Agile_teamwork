from django.contrib import admin
from .models import Post, Comment, CategoryPost, Like


class PostAdmin(admin.ModelAdmin):
    pass
    # prepopulated_fields = {"slug": ("title",)}


admin.site.register(Post, PostAdmin)

admin.site.register(Comment)


class CategoryPostAdmin(admin.ModelAdmin):
    pass
    # prepopulated_fields = {"slug": ("name",)}


admin.site.register(CategoryPost, CategoryPostAdmin)
admin.site.register(Like)
