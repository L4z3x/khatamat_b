# Generated by Django 5.1.2 on 2024-11-01 12:44

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0003_brothershiprequest_updated_at_joinrequest_updated_at_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='brothershiprequest',
            unique_together={('brother', 'owner')},
        ),
    ]
