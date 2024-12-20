# Generated by Django 5.1.2 on 2024-12-02 20:19

import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=20, unique=True)),
                ('fullname', models.CharField(max_length=30)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('gender', models.CharField(choices=[('male', 'M'), ('female', 'F')], default='M', max_length=7)),
                ('country', models.CharField(choices=[('Algeria', 'DZ')], default='DZ', max_length=20)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('profilePic', models.ImageField(default='UserProfilePic/default.png', upload_to='UserPofilePic')),
                ('khatmasNum', models.IntegerField(default=0)),
                ('brothersNum', models.IntegerField(default=0)),
                ('private', models.BooleanField(default=False)),
                ('blocked', models.ManyToManyField(default=None, to=settings.AUTH_USER_MODEL)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='brothership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brother_since', models.DateTimeField(default=django.utils.timezone.now)),
                ('user1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='brothership_initiated', to=settings.AUTH_USER_MODEL)),
                ('user2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='brothership_received', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Brothership',
                'unique_together': {('user1', 'user2')},
            },
        ),
        migrations.AddField(
            model_name='myuser',
            name='brothers',
            field=models.ManyToManyField(related_name='brothers_set', through='api.brothership', to=settings.AUTH_USER_MODEL),
        ),
    ]
