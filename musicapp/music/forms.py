from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import *


class SignupForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['playlist_title', 'playlist_user', 'playlist_scope']


class Song(forms.ModelForm):
    class Meta:
        model = Song
        fields = [
            'song_title', 'song_artist', 'song_duration', 'song_scope',
            'song_released_on'
        ]


class Follow(forms.ModelForm):
    class Meta:
        model = Follow
        fields = [
            'user',
            'follower',
        ]