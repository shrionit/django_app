from django.db import models
from django.contrib.auth.models import User
SCOPE = [('PUBLIC', 'PUBLIC'), ('PRIVATE', 'PRIVATE'),
         ('FOLLOWERS', 'FOLLOWERS')]


class Song(models.Model):
    song_title = models.CharField(max_length=250)
    song_artist = models.CharField(max_length=250)
    song_duration = models.TimeField(null=True)
    song_scope = models.CharField(max_length=20, choices=SCOPE)
    song_released_on = models.DateField(blank=True, null=True)
    song_added_by = models.ForeignKey(User,
                                      null=True,
                                      on_delete=models.CASCADE)


class Playlist(models.Model):
    playlist_title = models.CharField(max_length=250)
    playlist_user = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist_scope = models.CharField(max_length=20, choices=SCOPE)


class Playlist_Song(models.Model):
    playlist_id = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    playlist_song_id = models.ForeignKey(Song, on_delete=models.CASCADE)
