# Generated by Django 5.1.1 on 2024-09-09 21:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_rename_is_jonseeker_customuser_is_jobseeker_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='username',
        ),
    ]
