# Generated by Django 3.1.4 on 2021-01-15 02:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MW_STATS', '0007_auto_20210106_1835'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivateUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first', models.IntegerField(default=0)),
                ('second', models.IntegerField(default=0)),
                ('third', models.IntegerField(default=0)),
                ('total', models.IntegerField(default=0)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MW_STATS.privateusers')),
            ],
        ),
    ]
