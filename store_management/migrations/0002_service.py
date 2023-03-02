# Generated by Django 4.1.7 on 2023-03-02 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('store', models.ManyToManyField(to='store_management.store')),
            ],
        ),
    ]
