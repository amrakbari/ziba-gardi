# Generated by Django 4.1.7 on 2023-02-19 11:49

import accounts.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_role_customuser_role'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customuser',
            managers=[
                ('objects', accounts.models.CustomUserManager()),
            ],
        ),
    ]
