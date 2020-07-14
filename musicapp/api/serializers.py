from django.contrib.auth.models import Group, User
from rest_framework import serializers
from rest_framework.relations import RelatedField

from music.models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = [
            'id',
            'song_title',
            'song_artist',
            'song_duration',
            'song_file',
            'song_scope',
            'song_cover',
            'song_released_on',
            'song_added_by',
        ]


class SongListSerializer(serializers.RelatedField):
    def to_representation(self, value):
        value = value.playlist_song
        s = {
            'id': value.id,
            'song_title': value.song_title,
            'song_artist': value.song_artist,
            'song_duration': value.song_duration,
            # 'song_file': value.song_file.url,
            'song_scope': value.song_scope,
            # 'song_cover': value.song_cover.url,
            'song_released_on': value.song_released_on,
            'song_added_by': value.song_added_by.username,
        }
        return s


class PlaylistSerializer(serializers.ModelSerializer):
    playlist_song_set = SongListSerializer(many=True, read_only=True)

    class Meta:
        model = Playlist
        fields = [
            'id',
            'playlist_title',
            'playlist_user',
            'playlist_scope',
            'playlist_song_set',
        ]


class PlaylistSongListingField(serializers.RelatedField):
    def to_representation(self, value):
        s = {
            'id': value.id,
            'song_title': value.song_title,
            'song_artist': value.song_artist,
            'song_duration': value.song_duration,
            # 'song_file': value.song_file.url,
            'song_scope': value.song_scope,
            # 'song_cover': value.song_cover.url,
            'song_released_on': value.song_released_on,
            'song_added_by': value.song_added_by.username,
        }
        return s


class PlaylistListingField(serializers.RelatedField):
    def to_representation(self, value):
        s = {
            'id': value.id,
            'title': value.playlist_title,
        }
        return s


class PlaylistSongSerializer(serializers.ModelSerializer):
    playlist_song = PlaylistSongListingField(read_only=True)
    playlist = PlaylistListingField(read_only=True)

    class Meta:
        model = Playlist_Song
        fields = [
            'playlist',
            'playlist_song',
        ]
