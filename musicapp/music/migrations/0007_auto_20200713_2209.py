# Generated by Django 3.0.8 on 2020-07-13 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0006_auto_20200713_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='song_duration',
            field=models.CharField(default='00:00', max_length=6),
        ),
    ]
