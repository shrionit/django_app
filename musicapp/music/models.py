from django.db import models
from django.contrib.auth.models import User
SCOPE = [('PUBLIC', 'PUBLIC'), ('PRIVATE', 'PRIVATE'),
         ('FOLLOWERS', 'FOLLOWERS')]
from django.utils import timezone


class Song(models.Model):
    song_title = models.CharField(max_length=250)
    song_artist = models.CharField(max_length=250)
    song_duration = models.CharField(max_length=6, default='00:00')
    song_file = models.FileField(blank=True, null=True)
    song_scope = models.CharField(max_length=20, choices=SCOPE)
    song_released_on = models.CharField(max_length=4, blank=True, null=True)
    song_cover = models.ImageField(blank=True, null=True, upload_to='img')
    song_added_by = models.ForeignKey(User,
                                      null=True,
                                      on_delete=models.CASCADE)

    def __str__(self):
        return self.song_title


class Playlist(models.Model):
    playlist_title = models.CharField(max_length=250, unique=True)
    playlist_user = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist_scope = models.CharField(max_length=20, choices=SCOPE)
    playlist_created_on = models.DateTimeField(default=timezone.now)


class Playlist_Song(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    playlist_song = models.ForeignKey(Song, on_delete=models.CASCADE)
    playlist_song_order = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = [
            'playlist_song_order',
        ]
        ordering = [
            'playlist_song_order',
        ]
