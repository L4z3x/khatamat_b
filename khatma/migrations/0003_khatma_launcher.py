# Generated by Django 5.1.2 on 2024-11-11 21:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('khatma', '0002_khatmagroupsettings_message_delete_hizbslist_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='khatma',
            name='launcher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='launched_khatmas', to=settings.AUTH_USER_MODEL),
        ),
    ]
