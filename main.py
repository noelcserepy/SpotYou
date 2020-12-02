from yt_client import YTClient
from spotify_client import SpotifyClient

spotify = SpotifyClient()
yt = YTClient()


print(spotify.get_playlists())



