# Generated by Django 5.1.2 on 2024-10-12 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('khatma', '0006_alter_khatma_period'),
    ]

    operations = [
        migrations.AlterField(
            model_name='khatma',
            name='name',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
