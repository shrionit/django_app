from django.contrib.auth.models import User, Group
from rest_framework import serializers
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


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = [
            'id',
            'playlist_title',
            'playlist_user',
            'playlist_scope',
        ]