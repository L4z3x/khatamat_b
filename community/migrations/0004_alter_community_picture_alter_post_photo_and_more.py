# Generated by Django 5.1.2 on 2024-10-31 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0003_alter_community_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='picture',
            field=models.ImageField(null=True, upload_to='./communityIMG/<django.db.models.fields.CharField>'),
        ),
        migrations.AlterField(
            model_name='post',
            name='photo',
            field=models.ImageField(upload_to='./postImg/<django.db.models.fields.TextField>'),
        ),
        migrations.AlterField(
            model_name='post',
            name='video',
            field=models.FileField(upload_to='./postVideo/<django.db.models.fields.TextField>'),
        ),
    ]
