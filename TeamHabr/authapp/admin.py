from django.contrib import admin
from .models import User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'surname', 'status_block', 'status_update', 'date_create', 'date_update')
    search_fields = ('username', 'name',)

admin.site.register(User, UserAdmin)