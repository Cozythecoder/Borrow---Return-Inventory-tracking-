# Generated by Django 5.0.7 on 2024-07-10 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_register', '0003_alter_employee_duration_alter_employee_emp_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='duration',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='employee',
            name='emp_id',
            field=models.CharField(max_length=6),
        ),
    ]
