# Generated by Django 3.0.7 on 2021-11-15 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('placement', '0003_auto_20200930_1353'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='author',
        ),
    ]
