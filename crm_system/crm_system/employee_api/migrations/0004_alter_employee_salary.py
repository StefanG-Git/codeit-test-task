# Generated by Django 4.1.4 on 2022-12-17 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_api', '0003_alter_employee_salary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='salary',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
