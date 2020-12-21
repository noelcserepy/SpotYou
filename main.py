import pickle

from yt_client import YTClient
from spotify_client import SpotifyClient



# make web auth flow (no need for copy pasting link in cmd)
spotify = SpotifyClient()
yt = YTClient()


class Playlist():
    def __init__(self, pl):
        self.spotify_id = pl["id"]
        self.name = pl["name"]
        self.song_names = []
        self.yt_song_ids = []
        self.yt_id = None

        self._get_song_names()
        self._search_songs()
        self._make_new_playlist()
        self._add_songs_to_yt()


    def _get_song_names(self):
        songs = spotify.get_playlist_songs(self.spotify_id)

        for song in songs:
            artist_name = song["track"]["artists"][0]["name"]
            song_name = song["track"]["name"]

            search_q = f"{artist_name} - {song_name}"

            self.song_names.append(search_q)
        
        
    def _search_songs(self):
        song_ids = yt.find_songs(self.song_names)
        self.yt_song_ids.append(song_ids)


    def _make_new_playlist(self):
        self.yt_id = yt.make_playlist(self.name)


    def _add_songs_to_yt(self):
        with open("ids.pickle", "wb") as f:
            print("Saving yt_song_ids for Future Use...")
            pickle.dump(self.yt_song_ids, f)

        yt.add_songs(self.yt_song_ids, self.name)
        

    def add_saved_to_yt(self):
        with open("ids.pickle", "rb") as ids:
            print("Loading IDs...")
            self.yt_song_ids = pickle.load(ids)

        yt.add_songs(self.yt_song_ids, self.name)



playlists = spotify.get_playlists()

def convert_all_playlists():
    for playlist in playlists:
        Playlist(playlist)


def convert_first_playlist():
    Playlist(playlists[0])




