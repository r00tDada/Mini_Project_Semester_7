# Generated by Django 3.1 on 2021-11-25 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcell', '0002_company_visited_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='company_ctc',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='company',
            name='job_eligibility',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='company',
            name='job_profile',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='company',
            name='job_skills',
            field=models.CharField(max_length=1000),
        ),
    ]
