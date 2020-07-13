from django.contrib.auth.models import User, Group
from rest_framework import viewsets, status
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from .serializers import UserSerializer, GroupSerializer, SongSerializer, PlaylistSerializer
from music.models import *
from tinytag import TinyTag
from PIL import Image
import os
from django.core.files.base import ContentFile
import io


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


@csrf_exempt
@api_view(['GET'])
def song_list(request, uid):
    try:
        usr = User.objects.get(id=uid)
    except User.DoesNotExist:
        return HttpResponse(status=404)
    if usr.is_authenticated:
        songs = usr.song_set.all()
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)


@csrf_exempt
@api_view(['PUT'])
def update_song(request, uid, sid):
    try:
        usr = User.objects.get(id=uid)
    except User.DoesNotExist:
        return HttpResponse(status=404)
    if usr.is_authenticated:
        try:
            song = Song.objects.get(id=sid)
        except Song.DoesNotExist:
            return HttpResponse(status=404)
        serializer = SongSerializer(song, data=request.data)
        notify = {}
        if serializer.is_valid():
            serializer.save()
            notify['Success'] = 'Song update successful.'
            return Response(data=notify)
        return Response(serializer.errors, status=400)
    return Response(data={'Error': f'User {uid} doesn\'t exist.'})


@csrf_exempt
@api_view(['POST'])
def add_song(request, uid):
    print('FILES: ', request.FILES)
    try:
        usr = User.objects.get(id=uid)
    except User.DoesNotExist:
        return HttpResponse(status=404)
    if usr.is_authenticated:
        songfile = request.FILES['songfile']
        newsong = Song(song_title=songfile.name[:-4],
                       song_scope='PUBLIC',
                       song_added_by=usr)
        newsong.song_file.save(songfile.name, songfile, save=True)
        tag = TinyTag.get(newsong.song_file.url[1:], image=True)
        newsong.song_artist = tag.artist or 'Unknown'
        newsong.song_duration = convert(tag.duration)
        newsong.song_released_on = tag.year
        newsong.save()
        cover = tag.get_image()
        if cover:
            newsong.song_cover.save(songfile.name[:-4] + '_cover.jpg',
                                    ContentFile(io.BytesIO(cover).getvalue()),
                                    save=True)
        else:
            with open('media/img/default-cover.jpg', 'rb') as f:
                newsong.song_cover.save('default-cover.jpg', f, save=True)
    data = {
        'chunkIndex': 0,  # the chunk index processed
        'initialPreview': '',  #the thumbnail preview data (e.g. image)
        'initialPreviewConfig': {
            'type': 'audio',  # check previewTypes
            'caption': request.FILES['songfile'].name,  # caption
            'key': request.data['fileId'],  # keys for deleting/reorg preview
            'fileId': request.data['fileId'],  # file identifier
            'size': request.FILES['songfile'].size,  # file size
            'zoomData': '',  # separate larger zoom data
        }
    }
    return Response(data=data)


@csrf_exempt
@api_view(['DELETE'])
def delete_song(request, uid, sid):
    data = {}
    try:
        usr = User.objects.get(id=uid)
    except User.DoesNotExist:
        return HttpResponse(status=404)
    if usr.is_authenticated:
        try:
            song = Song.objects.get(id=sid)
        except Song.DoesNotExist:
            return Response(data={'Error': 'File didn\'t existed'}, status=404)
        song_file = song.song_file
        deleted = song.delete()
        if deleted:
            if os.path.exists(song_file.url[1:]):
                os.remove(song_file.url[1:])
                data['info'] = 'File existed'
            else:
                data['info'] = 'File didn\'t existed'
            data['Success'] = 'Delete Successful.'
        else:
            data['Failure'] = "Delete Unsuccessful."
    return Response(data=data)


@csrf_exempt
@api_view(['GET'])
def get_playlist(request, uid, pid=None):
    pass


@csrf_exempt
@api_view(['POST'])
def create_playlist(request, uid):
    pass


@csrf_exempt
@api_view(['PUT'])
def update_playlist(request, uid, pid):
    pass


@csrf_exempt
@api_view(['DELETE'])
def delete_playlist(request, uid):
    pass


# helper functions
def convert(seconds):
    hours = seconds // 3600
    seconds %= 3600
    mins = seconds // 60
    seconds %= 60
    return f'{int(mins)}:{int(seconds)}'