from django.urls import include, path
from django.contrib import admin
from . import views

app_name = 'music'

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('signup', views.register_view, name='signup'),
    path('home', views.home_view, name='home'),
    path('playlists', views.playlist_view, name='playlist'),
    path('playlists/<pid>', views.playlistsong_view, name='playlistsong'),
    path('songs', views.songs_view, name='songs'),
    path('accounts/logout', views.logout_view, name='logout'),
]
