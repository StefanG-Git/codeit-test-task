# Generated by Django 4.1.4 on 2022-12-17 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee_api', '0006_rename_company_id_employee_company_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='company_name',
            new_name='company_id',
        ),
    ]
