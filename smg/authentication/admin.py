from django.contrib import admin
from .models import User


class UserModelAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'department', 'is_manager')


admin.site.register(User, UserModelAdmin)
