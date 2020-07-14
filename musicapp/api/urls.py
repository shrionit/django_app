from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'songs', views.SongViewSet)
router.register(r'playlists', views.PlaylistViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls',
                              namespace='rest_framework')),
    path('songlist/<uid>', views.song_list, name='songList'),
    path('addsong/<uid>', views.add_song, name='addSong'),
    path('playlistsongs/',
         views.PlaylistSongListView.as_view(),
         name='playlistsonglist'),
    path('playlistsongs/<pk>',
         views.PlaylistSongList.as_view(),
         name='playlistsong'),

    # song rest
    path('deletesong/<uid>/<sid>', views.delete_song, name='deleteSong'),
    path('updatesong/<uid>/<sid>', views.update_song, name='updateSong'),

    # playlist rest
    path('getplaylist/<uid>/<pid>', views.get_playlist, name='getPlaylist'),
    path('addplaylist/<uid>', views.create_playlist, name='addPlaylist'),
    path('updateplaylist/<uid>/<pid>',
         views.update_playlist,
         name='updatePlaylist'),
    path('deleteplaylist/<uid>/<pid>',
         views.delete_playlist,
         name='deletePlaylist'),
]