# Generated by Django 4.1.7 on 2023-04-06 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store_management', '0009_userprofile_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='deleted_at',
        ),
    ]