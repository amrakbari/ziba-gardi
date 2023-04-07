# Generated by Django 4.1.7 on 2023-04-06 10:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_address_deleted_at_alter_customuser_deleted_at'),
        ('store_management', '0007_remove_stylistprofile_id_remove_usualuserprofile_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('birth_date', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('deleted_at', models.DateTimeField(default=None, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='usualuserprofile',
            name='user',
        ),
        migrations.AlterField(
            model_name='appointment',
            name='user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='store_management.userprofile'),
        ),
        migrations.AlterField(
            model_name='store',
            name='stylist',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store_management.userprofile'),
        ),
        migrations.DeleteModel(
            name='StylistProfile',
        ),
        migrations.DeleteModel(
            name='UsualUserProfile',
        ),
    ]
