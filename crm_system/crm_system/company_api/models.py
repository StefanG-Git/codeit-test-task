from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=30, unique=True)
    logo = models.ImageField(upload_to='company_logos/', default='uploads/default.jpg')
    description = models.TextField(max_length=300)

    def __str__(self):
        return self.name
