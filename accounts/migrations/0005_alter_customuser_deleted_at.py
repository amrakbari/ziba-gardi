# Generated by Django 4.1.7 on 2023-03-30 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_address_remove_customuser_role_customuser_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='deleted_at',
            field=models.DateTimeField(),
        ),
    ]
