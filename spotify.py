import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint

scope = "playlist-modify-public user-read-recently-played user-read-playback-state user-top-read app-remote-control user-modify-playback-state user-read-currently-playing user-read-playback-position playlist-read-collaborative streaming"

sp_auth=SpotifyOAuth(scope=scope, client_id='0f0fe3f41d224afa9a240b7334554e81', client_secret='8fd204363741445ea49e24cdc6f6adbb', redirect_uri='http://localhost:8000')

url = sp_auth.get_authorize_url()

sp = spotipy.Spotify(auth_manager=sp_auth)

# auth_token=sp_auth.get_cached_token()


# sp = spotipy.Spotify(auth=auth_token['access_token'])

user_id = sp.me()['id']

# sp.user_playlist_create(user_id, 'prixa')

search_str = "post malone"


result = sp.devices()
result = sp.search(search_str, type='track', limit=1)
# sp.start_playback(uris=['spotify:track:7xtQ8pzfF0eUtBx1KQUvRq'])
r=result['tracks']['items'][0]['name']
r2=result['tracks']['items'][0]['album']['images'][0]['url']
print(r2)