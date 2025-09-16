from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'company', 'is_active', 'is_superuser')
    list_display_links = ('id', 'email')