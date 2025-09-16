from django.db import models
from django.conf import settings


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    inn = models.CharField(max_length=12, unique=True)
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_company'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
