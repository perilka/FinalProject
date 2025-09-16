from django.contrib import admin
from companies.models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'inn', 'owner', 'created_at', 'updated_at')
    list_display_links = ('id', 'name')