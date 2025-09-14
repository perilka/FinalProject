from django.contrib import admin
from .models import User, Company, Storage

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'is_active', 'is_superuser')
    list_display_links = ('id', 'email')

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'inn', 'owner', 'created_at', 'updated_at')
    list_display_links = ('id', 'name')


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'company', 'created_at', 'updated_at')
    list_display_links = ('id', 'address')