# Generated by Django 5.1.2 on 2024-10-29 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('khatma', '0002_remove_khatma_period_khatma_duaa_khatma_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='khatma',
            name='duaa',
            field=models.CharField(default=None, max_length=180),
        ),
        migrations.AlterField(
            model_name='khatma',
            name='end_Date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='khatma',
            name='intentions',
            field=models.CharField(default=None, max_length=180),
        ),
        migrations.AlterField(
            model_name='khatma',
            name='start_Date',
            field=models.DateTimeField(),
        ),
    ]
