# Generated by Django 3.0.8 on 2020-07-14 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0010_auto_20200713_2338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='playlist_title',
            field=models.CharField(max_length=250, unique=True),
        ),
    ]
