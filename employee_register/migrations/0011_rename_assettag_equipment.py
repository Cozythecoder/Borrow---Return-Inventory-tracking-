# Generated by Django 5.0.7 on 2024-08-06 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee_register', '0010_assettag'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Assettag',
            new_name='Equipment',
        ),
    ]
