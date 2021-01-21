from django.contrib import admin
from .models import User, StatusUser
# Register your models here.

admin.site.register(User)
admin.site.register(StatusUser)