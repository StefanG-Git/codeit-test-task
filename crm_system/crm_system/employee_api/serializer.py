from datetime import date

from rest_framework import serializers

from crm_system.common.utils import *
from crm_system.employee_api.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    EMPLOYEE_MIN_YEARS = 18
    EMPLOYEE_MAX_YEARS = 65

    PHOTO_MAX_SIZE_IN_MB = 3

    SALARY_MIN_VALUE = 500

    class Meta:
        model = Employee
        fields = '__all__'

    def validate_first_name(self, first_name):
        if not string_contains_only_letters(first_name):
            raise serializers.ValidationError('First name must contains only letters')

        return first_name.capitalize()

    def validate_last_name(self, last_name):
        if not string_contains_only_letters(last_name):
            raise serializers.ValidationError('Last name must contains only letters')

        return last_name.capitalize()

    def validate_date_of_birth(self, date_of_birth):
        today = date.today()
        if today < date_of_birth:
            raise serializers.ValidationError('Invalid date')

        employee_age = calculate_years_between_dates(date_of_birth, today)
        if employee_age < self.EMPLOYEE_MIN_YEARS:
            raise serializers.ValidationError('People under age of 18 cannot work')
        if self.EMPLOYEE_MAX_YEARS < employee_age:
            raise serializers.ValidationError('People older than 65 cannot work')

        return date_of_birth

    def validate_photo(self, image):
        if not image_size_is_valid(image, self.PHOTO_MAX_SIZE_IN_MB):
            raise serializers.ValidationError(f'Max file size is {self.PHOTO_MAX_SIZE_IN_MB}MB')

        return image

    def validate_salary(self, salary):
        if salary < self.SALARY_MIN_VALUE:
            raise serializers.ValidationError(f'The minimum wage is {self.SALARY_MIN_VALUE} USD')

        return salary
