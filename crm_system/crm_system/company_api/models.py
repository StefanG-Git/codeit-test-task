from django.db import models


class Company(models.Model):
    NAME_MAX_LENGTH = 30
    DESCRIPTION_MAX_LENGTH = 300
    LOGO_UPLOAD_FOLDER = 'company_logos/'

    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    logo = models.ImageField(upload_to=LOGO_UPLOAD_FOLDER)
    description = models.TextField(max_length=DESCRIPTION_MAX_LENGTH)

    def __str__(self):
        return self.name
