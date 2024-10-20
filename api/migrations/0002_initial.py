# Generated by Django 5.1.2 on 2024-10-20 08:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('api', '0001_initial'),
        ('khatma', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='joinrequest',
            name='khatmaGroup',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='khatma.khatmagroup'),
        ),
        migrations.AddField(
            model_name='joinrequest',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='JoinRequest_owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='joinrequest',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='notification',
            name='Kh',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='khatma.khatma'),
        ),
        migrations.AddField(
            model_name='notification',
            name='kh_G',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='khatma.khatmagroup'),
        ),
        migrations.AddField(
            model_name='notification',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification_from', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notification_to', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='joinrequest',
            unique_together={('user', 'khatmaGroup', 'owner')},
        ),
    ]
