# Generated by Django 3.0.8 on 2020-07-14 09:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0011_auto_20200714_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='playlist_created_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
