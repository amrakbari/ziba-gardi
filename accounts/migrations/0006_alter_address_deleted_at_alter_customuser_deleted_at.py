# Generated by Django 4.1.7 on 2023-03-30 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_customuser_deleted_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='deleted_at',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='deleted_at',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
