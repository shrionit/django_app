from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import SignupForm
from .models import *

POST, GET = 'POST', 'GET'


def index(request):
    usr = request.user
    if usr is not None:
        if usr.is_authenticated:
            return redirect('music:home')
    return redirect('music:login')


def login_view(request):
    usr = request.user
    if usr is not None:
        if usr.is_authenticated:
            return redirect('music:home')

    form = AuthenticationForm(request.POST or None)
    if request.method == POST:
        user_name = request.POST['username']
        user_pass = request.POST['password']
        usr = authenticate(request, username=user_name, password=user_pass)
        if usr is not None:
            login(request, usr)
            return redirect('music:home')
        else:
            return render(request, 'accounts/login.html', {
                'red': True,
                'data': form.error_messages,
                'form': form,
            })
    else:
        return render(request, 'accounts/login.html', {
            'form': form,
            'red': False,
        })


def register_view(request):
    form = SignupForm(request.POST or None)
    if request.method == POST:
        print(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.active = True
            user.staff = False
            user.admin = False
            user.save()
            login(request, user)
            return render(request, 'music/home.html')
    return render(
        request,
        'accounts/signup.html',
        {
            'form': form,
        },
    )


def logout_view(request):
    logout(request)
    return render(request, 'accounts/logout.html')


@login_required(login_url='/music/')
def home_view(request):
    usr = request.user
    is_logged_in = usr.is_authenticated
    otheruserplaylist = []
    followingplaylist = []
    followings = Follow.objects.filter(follower=usr)
    followers = Follow.objects.filter(user=usr)
    myfollowings = []
    myfollowers = []
    for f in followings:
        myfollowings.append(f.user)
    for f in followers:
        myfollowers.append(f.user)

    for u in User.objects.filter(is_superuser=False).exclude(id=usr.id):
        for pl in u.playlist_set.filter(playlist_scope='PUBLIC'):
            otheruserplaylist.append(pl)
    for u in myfollowings:
        for p in u.playlist_set.filter(playlist_scope='FOLLOWERS'):
            followingplaylist.append(p)

    return render(
        request, 'music/home.html', {
            'pg_active': True,
            'otheruserplaylist': otheruserplaylist,
            'followingplaylist': followingplaylist,
            'myfollowers': myfollowers,
            'myfollowings': myfollowings,
        })


@login_required(login_url='/music/')
def songs_view(request):
    return render(request, 'music/songs.html', {
        'pg_active': True,
    })


@login_required(login_url='/music/')
def playlist_view(request):
    follow = Follow.objects.filter(follower=request.user)
    playlistdata = []
    for u in [fl.user for fl in follow]:
        for pl in u.playlist_set.filter(playlist_scope='FOLLOWERS'):
            playlistdata.append(pl)
    print(playlistdata)
    return render(request, 'music/playlist.html', {
        'pg_active': True,
        'playlistview': False,
        'playlistdata': playlistdata,
    })


@login_required(login_url='/music/')
def playlistsong_view(request, pid):
    plist = Playlist.objects.get(id=pid).playlist_song_set.all()
    playlist = []
    for ls in plist:
        playlist.append(ls.playlist_song)
    return render(
        request, 'music/playlist.html', {
            'pg_active': True,
            'playlistview': True,
            'playlistid': pid,
            'playlistsongs': playlist,
        })
