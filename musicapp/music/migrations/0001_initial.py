# Generated by Django 3.0.3 on 2020-07-09 19:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playlist_title', models.CharField(max_length=250)),
                ('playlist_scope', models.CharField(choices=[('PUBLIC', 'PUBLIC'), ('PRIVATE', 'PRIVATE'), ('FOLLOWERS', 'FOLLOWERS')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('song_title', models.CharField(max_length=250)),
                ('song_artist', models.CharField(max_length=250)),
                ('song_duration', models.TimeField(null=True)),
                ('song_scope', models.CharField(choices=[('PUBLIC', 'PUBLIC'), ('PRIVATE', 'PRIVATE'), ('FOLLOWERS', 'FOLLOWERS')], max_length=20)),
                ('song_released_on', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=50)),
                ('user_email', models.CharField(max_length=100)),
                ('user_pass', models.CharField(max_length=35)),
            ],
        ),
        migrations.CreateModel(
            name='Playlist_Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playlist_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.Playlist')),
                ('playlist_song_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.Song')),
            ],
        ),
        migrations.AddField(
            model_name='playlist',
            name='playlist_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.User'),
        ),
    ]
