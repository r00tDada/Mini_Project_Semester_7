# Generated by Django 3.1 on 2021-11-24 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_profile_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='user_type',
            field=models.CharField(default='Student', max_length=20),
        ),
    ]
