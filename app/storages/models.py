from django.db import models

class Storage(models.Model):
    address = models.CharField(max_length=255)
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.CASCADE,
        related_name='storages'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.address} ({self.company.name})"

