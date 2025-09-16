from django.contrib import admin
from storages.models import Storage


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'company', 'created_at', 'updated_at')
    list_display_links = ('id', 'address')
