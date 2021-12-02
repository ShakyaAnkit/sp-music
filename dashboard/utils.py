import spotipy
from spotipy.oauth2 import SpotifyOAuth

from django.conf import settings as conf_settings

from .models import CurrentPlayBack, FeaturedTrack, PlayListTrack

def get_sp():
    scope = "playlist-modify-public user-read-recently-played user-read-playback-state user-top-read app-remote-control user-modify-playback-state user-read-currently-playing user-read-playback-position playlist-read-collaborative streaming"
            
    sp_auth=SpotifyOAuth(scope=scope, client_id=conf_settings.SPOTIFY_CLIENT_ID, client_secret=conf_settings.SPOTIFY_CLIENT_SECRET, redirect_uri='http://localhost:8000/dashboard/')

    url = sp_auth.get_authorize_url()

    # sp = spotipy.Spotify(auth_manager=sp_auth)

    auth_token=sp_auth.get_cached_token()

    sp = spotipy.Spotify(auth=auth_token['access_token'])

    return sp

def get_device():
    device_id = None
    device_list = get_sp().devices()['devices']
    print(device_list,111111111111111111111111)
    if len(device_list) > 0:
        for device in device_list:
            if device['is_active']:
                device_id= device['id']
    return device_id

def get_current_playback():
    current_playback_info = get_sp().current_playback(market=None, additional_types=None)
    if current_playback_info:
        current_playback = CurrentPlayBack.from_playback(current_playback_info)
        return current_playback
    return None

def get_featured_tracks():
    devices = get_sp().devices()
    tracks = []
    featured_playlists = get_sp().new_releases(country='NP', limit=12, offset=0)
    if featured_playlists:
        for track_info in featured_playlists['albums']['items']:
            track = FeaturedTrack.from_track(track_info)
            tracks.append(track)
    return tracks

def get_playlist_tracks():
    tracks = []
    playlist_tracks = get_sp().user_playlist(user='ehfc7cnf8bizgh9gm0xysqn7g', playlist_id='3I0WxSdjhz4kwnoTPC9e6l')
    if playlist_tracks:
        for track_info in playlist_tracks['tracks']['items']:
            track = PlayListTrack.from_track(track_info, playlist_tracks['uri'])
            tracks.append(track)
    return tracks