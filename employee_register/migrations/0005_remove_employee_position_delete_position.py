# Generated by Django 5.0.7 on 2024-07-10 15:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee_register', '0004_alter_employee_duration_alter_employee_emp_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='position',
        ),
        migrations.DeleteModel(
            name='Position',
        ),
    ]
