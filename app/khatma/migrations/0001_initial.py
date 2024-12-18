# Generated by Django 5.1.2 on 2024-12-18 10:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('group', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Khatma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('endDate', models.DateTimeField()),
                ('intentions', models.CharField(default=None, max_length=180)),
                ('duaa', models.CharField(default=None, max_length=180)),
                ('startSurah', models.CharField(choices=[('the cow', 'the cow')], max_length=35)),
                ('startVerse', models.PositiveIntegerField(default=0)),
                ('endSurah', models.CharField(choices=[('the cow', 'the cow')], max_length=35)),
                ('endVerse', models.PositiveIntegerField(default=0)),
                ('progress', models.PositiveIntegerField(default=0)),
                ('status', models.CharField(choices=[('ongoing', 'ongoing'), ('completed', 'completed'), ('aborted', 'aborted')], max_length=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('group', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='group.group')),
                ('launcher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='launched_khatmas', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('name', 'group')},
            },
        ),
        migrations.CreateModel(
            name='khatmaCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=15, unique=True)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('expiration_date', models.DateTimeField(blank=True, null=True)),
                ('issued_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issued_khatma_codes', to=settings.AUTH_USER_MODEL)),
                ('khatma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='khatma.khatma')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='khatmaMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startShareSurah', models.CharField(choices=[('the cow', 'the cow')], max_length=35)),
                ('startShareVerse', models.PositiveIntegerField(default=0)),
                ('endShareSurah', models.CharField(choices=[('the cow', 'the cow')], max_length=35)),
                ('endShareVerse', models.PositiveIntegerField(default=0)),
                ('currentSurah', models.CharField(choices=[('the cow', 'the cow')], max_length=35)),
                ('currentVerse', models.PositiveIntegerField(default=0)),
                ('progress', models.PositiveIntegerField(default=0)),
                ('finishDate', models.DateTimeField(null=True)),
                ('status', models.CharField(choices=[('ongoing', 'ongoing'), ('completed', 'completed'), ('aborted', 'aborted')], default='ongoing', max_length=20)),
                ('groupMembership', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='khatmaMembership', to='group.groupmembership')),
                ('khatma', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='khatma.khatma')),
            ],
            options={
                'unique_together': {('khatma', 'groupMembership')},
            },
        ),
    ]
