# Generated by Django 3.0.8 on 2020-10-25 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facebook', '0003_auto_20201021_2055'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='img',
            field=models.TextField(blank=True, null=True),
        ),
    ]
