# Generated by Django 4.1.7 on 2023-07-14 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_address_deleted_at_alter_customuser_deleted_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Neighbourhood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='address',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='address',
            name='longitude',
        ),
        migrations.AddField(
            model_name='address',
            name='neighbourhood',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.neighbourhood'),
        ),
    ]