import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint

scope = "user-library-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
user = os.environ.get("SPOTIFY_USER_ID")


def main():
    liked_songs = get_liked_songs()
    playlist_songs = get_playlist_songs()
    pprint('# Liked songs: ' + str(len(liked_songs)))
    pprint('# Playlist songs: ' + str(len(playlist_songs)))

    missing_songs = liked_songs.difference(playlist_songs)
    pprint(missing_songs)


def get_liked_songs():
    all_liked_songs = set()
    liked_songs = sp.current_user_saved_tracks()
    while liked_songs:
        for item in liked_songs['items']:
            song_name_and_artist = item['track']['artists'][0]['name'] + " – " + item['track']['name']
            all_liked_songs.add(song_name_and_artist)
        if liked_songs['next']:
            liked_songs = sp.next(liked_songs)
        else:
            liked_songs = None
    return all_liked_songs


def get_playlist_songs():
    all_playlists_songs = set()
    playlists = sp.user_playlists(user=user)
    while playlists:
        for playlist in playlists['items']:
            playlist_songs = sp.playlist_items(playlist['uri'])
            while playlist_songs:
                for item in playlist_songs['items']:
                    song_name_and_artist = item['track']['artists'][0]['name'] + " – " + \
                                                                  item['track']['name']
                    all_playlists_songs.add(song_name_and_artist)
                if playlist_songs['next']:
                    playlist_songs = sp.next(playlist_songs)
                else:
                    playlist_songs = None
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None
    return all_playlists_songs


if __name__ == '__main__':
    main()

