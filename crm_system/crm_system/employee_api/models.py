from django.core.validators import MinLengthValidator
from django.db import models

from crm_system.company_api.models import Company


class Employee(models.Model):
    FIRST_NAME_MIN_LENGTH = 2
    FIRST_NAME_MAX_LENGTH = 30

    LAST_NAME_MIN_LENGTH = 2
    LAST_NAME_MAX_LENGTH = 30

    POSITION_MIN_LENGTH = 3
    POSITION_MAX_LENGTH = 50

    PHOTO_UPLOAD_FOLDER = 'employee_photos/'

    SALARY_MAX_DIGITS = 8
    SALARY_DECIMAL_PLACES = 2

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(FIRST_NAME_MIN_LENGTH),
        )
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(LAST_NAME_MIN_LENGTH),
        )
    )

    date_of_birth = models.DateField()

    photo = models.ImageField(upload_to=PHOTO_UPLOAD_FOLDER)

    position = models.CharField(
        max_length=POSITION_MAX_LENGTH,
        validators=(
            MinLengthValidator(POSITION_MIN_LENGTH),
        ),
    )

    salary = models.DecimalField(
        max_digits=SALARY_MAX_DIGITS,
        decimal_places=SALARY_DECIMAL_PLACES,
    )

    company_id = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'