# Generated by Django 4.2.3 on 2023-08-03 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_management', '0011_alter_userprofile_birth_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='store',
        ),
        migrations.AddField(
            model_name='store',
            name='services',
            field=models.ManyToManyField(to='store_management.service'),
        ),
    ]
