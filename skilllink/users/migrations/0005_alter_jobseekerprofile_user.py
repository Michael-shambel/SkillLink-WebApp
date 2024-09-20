# Generated by Django 5.1 on 2024-09-19 21:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_jobseekerprofile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobseekerprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
