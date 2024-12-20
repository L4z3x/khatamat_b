# Generated by Django 5.1.2 on 2024-11-22 08:47

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='community',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('authentications', models.CharField(choices=[('none', 'none'), ('custom', 'custom')], default='none', max_length=20)),
                ('picture', models.ImageField(null=True, upload_to='communityPic')),
                ('bio', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='communityMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('admin', 'admin'), ('user', 'user')], max_length=10)),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='membership', to='community.community')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='community',
            name='members',
            field=models.ManyToManyField(through='community.communityMembership', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=300)),
                ('body', models.TextField(max_length=3000)),
                ('status', models.CharField(max_length=10)),
                ('views', models.IntegerField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('photo', models.ImageField(upload_to='postPic')),
                ('video', models.FileField(upload_to='postVid')),
                ('comment_n', models.IntegerField()),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.community')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.communitymembership')),
            ],
        ),
        migrations.CreateModel(
            name='comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=3000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='community.comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.communitymembership')),
                ('post', models.ManyToManyField(to='community.post')),
            ],
        ),
    ]
