# Generated by Django 5.1 on 2024-09-16 12:54

import users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_customuser_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobseekerprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to=users.models.user_directory_path),
        ),
    ]
