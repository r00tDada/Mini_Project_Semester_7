# Generated by Django 3.2.9 on 2021-11-16 10:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default.jpg', upload_to='profile_pics')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('id_no', models.CharField(max_length=20)),
                ('phone_no', models.CharField(max_length=20)),
                ('cgpa', models.CharField(max_length=20)),
                ('degree', models.CharField(max_length=20)),
                ('stream', models.CharField(max_length=20)),
                ('placed_in', models.CharField(default='NoOffer', max_length=20)),
                ('docfile', models.FileField(default='Sourabh_Gupta.pdf', upload_to='Resume')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
