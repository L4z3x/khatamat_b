# Generated by Django 5.1.2 on 2024-11-07 09:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('khatma', '0007_rename_end_date_khatma_enddate_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(max_length=400000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='khatma.khatmagroup')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='khatma.khatmagroupmembership')),
            ],
        ),
    ]