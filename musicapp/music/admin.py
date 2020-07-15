from django.contrib import admin
from .models import *

admin.site.register(Song)
admin.site.register(Playlist)
admin.site.register(Playlist_Song)
admin.site.register(Follow)
