# Generated by Django 3.0.8 on 2020-10-25 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facebook', '0011_remove_post_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='comments',
            field=models.ManyToManyField(related_name='post_id', to='facebook.Comment'),
        ),
    ]
