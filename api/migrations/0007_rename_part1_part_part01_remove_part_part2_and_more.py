# Generated by Django 5.0.6 on 2024-07-06 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_part_part1'),
    ]

    operations = [
        migrations.RenameField(
            model_name='part',
            old_name='part1',
            new_name='part01',
        ),
        migrations.RemoveField(
            model_name='part',
            name='part2',
        ),
        migrations.RemoveField(
            model_name='part',
            name='part3',
        ),
        migrations.RemoveField(
            model_name='part',
            name='part4',
        ),
        migrations.RemoveField(
            model_name='part',
            name='part5',
        ),
        migrations.RemoveField(
            model_name='part',
            name='part6',
        ),
        migrations.RemoveField(
            model_name='part',
            name='part7',
        ),
        migrations.RemoveField(
            model_name='part',
            name='part8',
        ),
        migrations.RemoveField(
            model_name='part',
            name='part9',
        ),
        migrations.AddField(
            model_name='part',
            name='part02',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='part',
            name='part03',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='part',
            name='part04',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='part',
            name='part05',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='part',
            name='part06',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='part',
            name='part07',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='part',
            name='part08',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='part',
            name='part09',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='part',
            name='part10',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='part',
            name='part11',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='part',
            name='part12',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
