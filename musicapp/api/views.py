from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer, SongSerializer, PlaylistSerializer
from music.models import *


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited
    """
    queryset = User.objects.all().filter(
        is_superuser=False).order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class SongViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows songslist to be viewed or edited
    """
    queryset = Song.objects.all()
    serializer_class = SongSerializer


class PlaylistViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows playlist to be viewed or edited
    """
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer