from django.contrib.auth.models import User, Group
from rest_framework import viewsets, status
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import *
from music.models import *
from tinytag import TinyTag
from PIL import Image
import os
from django.core.files.base import ContentFile
import io, ast


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


class PlaylistSongList(generics.ListCreateAPIView):
    # queryset = Playlist.objects.all()
    def get_queryset(self):
        queryset = Playlist.objects.filter(
            id=self.kwargs["pk"])[0].playlist_song_set.all()
        return queryset

    serializer_class = PlaylistSongSerializer


class PlaylistSongListView(generics.ListCreateAPIView):
    def get_queryset(self):
        return Playlist.objects.all()

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
    try:
        usr = User.objects.get(id=uid)
    except User.DoesNotExist:
        return HttpResponse(status=404)
    if usr.is_authenticated:
        songfile = request.FILES['songfile']
        if not Song.objects.filter(song_title=songfile.name[:-4]).exists():
            newsong = Song.objects.get_or_create(id=Song.objects.count(),
                                                 song_title=songfile.name[:-4],
                                                 song_scope='PUBLIC',
                                                 song_added_by=usr)[0]
            newsong.song_file.save(songfile.name, songfile, save=True)
            tag = TinyTag.get(newsong.song_file.url[1:], image=True)
            newsong.song_artist = tag.artist or 'Unknown'
            newsong.song_duration = convert(tag.duration)
            newsong.song_released_on = tag.year
            newsong.save()
            cover = tag.get_image()
            if cover:
                newsong.song_cover.save(songfile.name[:-4] + '_cover.jpg',
                                        ContentFile(
                                            io.BytesIO(cover).getvalue()),
                                        save=True)
            else:
                with open('media/img/default-cover.jpg', 'rb') as f:
                    newsong.song_cover.save('default-cover.jpg', f, save=True)
        else:
            return Response({
                'Already': 'EXIST',
                'Error': 'Song Already Exist',
            })
    data = {
        'Already': '!EXIST',
        'chunkIndex': 0,  # the chunk index processed
        'initialPreview': '',  #the thumbnail preview data (e.g. image)
        'initialPreviewConfig': {
            'type': 'audio',  # check previewTypes
            'caption': request.FILES['songfile'].name,  # caption
            'key': request.data['fileId'],  # keys for deleting/reorg preview
            'fileId': request.data['fileId'],  # file identifier
            'size': request.FILES['songfile'].size,  # file size
            'zoomData': '',  # separate larger zoom data
        },
        'songinfo': {
            'songid': newsong.id,
            'songTitle': newsong.song_title,
            'songUser': usr.username,
            'songArtist': newsong.song_artist,
            'songDuration': newsong.song_duration,
            'songScope': newsong.song_scope,
            'songUrl': newsong.song_file.url,
            'songCoverUrl': newsong.song_cover.url,
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
        data['deletedsongid'] = sid
        if deleted:
            if os.path.exists(song_file.url[1:]):
                os.remove(song.song_cover.url[1:])
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
    try:
        usr = User.objects.get(id=uid)
    except User.DoesNotExist:
        return HttpResponse(status=404)
    if usr.is_authenticated:
        kw = request.data['kw'] or ''


@csrf_exempt
@api_view(['POST'])
def create_playlist(request, uid):
    try:
        usr = User.objects.get(id=uid)
    except User.DoesNotExist:
        return HttpResponse(status=404)
    if usr.is_authenticated:
        plisttitle = request.data['plistTitle']
        plistuser = usr
        plistscope = request.data['plistScope']
        count = Playlist.objects.count()
        playlist = None
        if count == 0:
            playlist = Playlist.objects.get_or_create(
                playlist_title=plisttitle,
                playlist_user=plistuser,
                playlist_scope=plistscope)
            return Response({
                'Already': '!EXIST',
                'Success': 'Playlist created.',
                'plistid': playlist.id,
                'plistTitle': playlist.playlist_title,
                'plistUser': usr.username,
                'plistScope': playlist.playlist_scope
            })
            playlist.save()
        else:
            if not Playlist.objects.filter(playlist_title=plisttitle).exists():
                playlist = Playlist.objects.get_or_create(
                    playlist_title=plisttitle,
                    playlist_user=plistuser,
                    playlist_scope=plistscope)[0]
                playlist.save()
                return Response({
                    'Already': '!EXIST',
                    'Success': 'Playlist created.',
                    'plistid': playlist.id,
                    'plistTitle': playlist.playlist_title,
                    'plistUser': usr.username,
                    'plistScope': playlist.playlist_scope
                })
            else:
                return Response({
                    'Already': 'EXIST',
                })
    return HttpResponse(status=404)


@csrf_exempt
@api_view(['PUT'])
def update_playlist(request, uid, pid):
    try:
        usr = User.objects.get(id=uid)
    except User.DoesNotExist:
        return HttpResponse(status=404)
    if usr.is_authenticated:
        if request.data['changename'] == True:
            newname = request.data['newname']
            if User.objects.get(id=uid).playlist_set.filter(id=pid).exists():
                plist = Playlist.objects.get(id=pid)
                plist.playlist_title = newname
                plist.save()
                return Response({
                    'Success': 'Playlist name changed',
                    'oldName': oldname,
                    'newName': newname,
                })
            else:
                return HttpResponse(status=404)

        plistid = request.data['plistId']
        playlist = Playlist.objects.get(id=pid)
        aobject = ast.literal_eval(request.data['songIds'])
        plistsongids = list(aobject) if type(aobject) is not int else [aobject]
        created = []
        data = {
            'Success': 'Songs added to playlist',
            'playlistname': playlist.playlist_title,
            'songsadded': [],
            'msg': []
        }
        for id in plistsongids:
            song = Song.objects.get(id=id)
            if not Playlist_Song.objects.filter(playlist=playlist,
                                                playlist_song=song).exists():
                plist = Playlist_Song.objects.get_or_create(
                    playlist=playlist, playlist_song=song)[0]
                data['songsadded'].append(id)
                created.append(plist)
            else:
                data['msg'].append(
                    f'{Song.objects.get(id=id).song_title} already exist in {Playlist.objects.get(id=pid).playlist_title}'
                )
        return Response(data)


@csrf_exempt
@api_view(['DELETE'])
def delete_playlist(request, uid, pid):
    try:
        usr = User.objects.get(id=uid)
    except User.DoesNotExist:
        return HttpResponse(status=404)
    if usr.is_authenticated:
        deleted = Playlist.objects.get(id=pid).delete()
        if deleted:
            return Response({
                'Success': 'Deleted',
                'deletedplaylistid': pid,
            })
        else:
            return HttpResponse(status=404)
    return HttpResponse(status=404)


@csrf_exempt
@api_view(['DELETE'])
def delete_playlistsong(request, uid, pid, sid):
    try:
        usr = User.objects.get(id=uid)
    except User.DoesNotExist:
        return HttpResponse(status=404)
    if usr.is_authenticated:
        song = Song.objects.get(id=sid)
        deleted = Playlist.objects.get(id=pid).playlist_song_set.get(
            playlist_song=song).delete()
        if deleted:
            return Response({
                'Success': 'Deleted',
                'playlistid': pid,
                'deletedplaylistsongid': sid,
            })
        else:
            return HttpResponse(status=404)
    return HttpResponse(status=404)


# helper functions
def convert(seconds):
    hours = seconds // 3600
    seconds %= 3600
    mins = seconds // 60
    seconds %= 60
    return f'{int(mins)}:{int(seconds)}'