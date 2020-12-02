import os 
import spotipy

from spotipy.oauth2 import SpotifyOAuth



client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")
scope = "playlist-read-private"


class SpotifyClient:
    def __init__(self):
        self.spotify = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=client_id, 
                client_secret=client_secret, 
                redirect_uri=redirect_uri,
                scope=scope
            )
        )


    def get_playlists(self):
        results = self.spotify.current_user_playlists()
        playlists = results["items"]
        while results["next"]:
            results = self.spotify.next(results)
            playlists.extend(results["items"])

        return playlists


    def get_playlist_songs(self, playlist_id):
        results = self.spotify.playlist_items(playlist_id)
        songs = results["items"]
        while results["next"]:
            results = self.spotify.next(results)
            songs.extend(results["items"])

        return songs

