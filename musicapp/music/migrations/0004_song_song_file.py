# Generated by Django 3.0.8 on 2020-07-12 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0003_song_song_added_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='song_file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]