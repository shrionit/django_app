# django_app

A music app

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```cmd
pip install -r requirements.txt
```

## Usage

Go to base ('musicapp/') and run

```cmd
python manage.py runserver
```

## Users

TWO_USERS

```cmd
admin: root@root
user0: user_0@Abcd_987654
user1: user_1@Abcd_987654
```

## [DRF] View

Use curl or open a webbrowser

```cmd
songs View:
    curl http://127.0.0.1:8000/api/songs/

playlists View:
    curl http://127.0.0.1:8000/api/playlists/

users View:
    curl http://127.0.0.1:8000/api/users/

groups View:
    curl http://127.0.0.1:8000/api/groups/
```
