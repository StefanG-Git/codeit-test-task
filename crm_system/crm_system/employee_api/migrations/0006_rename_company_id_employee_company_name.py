# Generated by Django 4.1.4 on 2022-12-17 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee_api', '0005_alter_employee_salary'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='company_id',
            new_name='company_name',
        ),
    ]
