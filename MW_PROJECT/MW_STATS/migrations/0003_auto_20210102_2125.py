# Generated by Django 3.1.4 on 2021-01-03 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MW_STATS', '0002_friends'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friends',
            name='friend',
        ),
        migrations.AddField(
            model_name='friends',
            name='gamertag1',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='friends',
            name='gamertag2',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='friends',
            name='gamertag3',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='friends',
            name='gamertag4',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='friends',
            name='gamertag5',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]