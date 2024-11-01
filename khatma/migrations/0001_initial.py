# Generated by Django 5.1.2 on 2024-10-20 08:14

import django.db.models.deletion
import khatma.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='hizbsList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('desc', models.CharField(max_length=150, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='khatmaGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, unique=True)),
                ('icon', models.ImageField(upload_to=khatma.models.upload_to)),
            ],
        ),
        migrations.CreateModel(
            name='thomonList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('desc', models.CharField(max_length=150, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Khatma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('period', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7')], default=None, max_length=10)),
                ('khatmaGroup', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='khatma.khatmagroup')),
            ],
            options={
                'unique_together': {('name', 'khatmaGroup')},
            },
        ),
        migrations.CreateModel(
            name='khatmaGroupMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('admin', 'admin'), ('user', 'user')], default='admin', max_length=6)),
                ('khatmaGroup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='khatma_G_membership', to='khatma.khatmagroup')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='khatmagroup',
            name='members',
            field=models.ManyToManyField(related_name='khatmaGroup', through='khatma.khatmaGroupMembership', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='khatmaMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('khatma', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='khatma.khatma')),
                ('khatmaGroupMembership', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='khatma.khatmagroupmembership')),
            ],
            options={
                'unique_together': {('khatma', 'khatmaGroupMembership')},
            },
        ),
    ]
