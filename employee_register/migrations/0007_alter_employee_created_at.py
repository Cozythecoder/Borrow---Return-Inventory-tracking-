# Generated by Django 5.0.7 on 2024-07-24 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_register', '0006_employee_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='created_at',
            field=models.DateTimeField(),
        ),
    ]