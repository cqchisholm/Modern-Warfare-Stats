# Generated by Django 3.1.4 on 2021-01-06 01:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MW_STATS', '0003_auto_20210102_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friends',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
