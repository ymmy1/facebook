# Generated by Django 3.0.8 on 2020-09-17 06:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0008_auto_20200916_2314'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='avatar',
        ),
    ]
