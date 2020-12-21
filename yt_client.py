import os
import pickle

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request



class YTClient():
    def __init__(self):
        self.clients_secrets_file = os.getenv("CLIENT_SECRET_PATH")
        self.credentials = None
        self.youtube = None
        
        self._authorize()


    def _authorize(self):
        if os.path.exists("token.pickle"):
            print("Loading Credentials From File...")
            with open("token.pickle", "rb") as token:
                self.credentials = pickle.load(token)

        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                print("Refreshing Access Token...")
                self.credentials.refresh(Request())
            else:
                print("Fetching New Tokens...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.clients_secrets_file, 
                    scopes=["https://www.googleapis.com/auth/youtube"]
                )

                flow.run_local_server(
                    port=8080, prompt="consent", authorization_prompt_message=""
                )
                credentials = flow.credentials

                with open("token.pickle", "wb") as f:
                    print("Saving Credentials for Future Use...")
                    pickle.dump(credentials, f)

        youtube = build("youtube", "v3", credentials=self.credentials)
        self.youtube = youtube


    def list_channels(self):
        self._authorize()

        request = self.youtube.channels().list(
            part="statistics",
            forUsername="TheHoinoel"
        )

        response = request.execute()

        print(response)


    def make_playlist(self, playlist_name):
        self._authorize()

        request_body = {
            "snippet": {
                "channelId": "UCeVKa9MfOuXxIkYanPukgig",
                "title": playlist_name,
                "defaultLanguage": "en",
            },
            "status": {
                "privacyStatus": "private"
            }
        }


        request = self.youtube.playlists().insert(
            part="snippet,status",
            body=request_body
        )
        
        response = request.execute()
        playlist_id = response["id"]

        return playlist_id


    def find_songs(self, title_list):
        self._authorize()
        id_list = []
        
        def batch_callback(request_id, response, exception):
            if exception is not None:
                print(exception)
            else:
                print(response)
                id_list.append(response["items"][0]["id"]["videoId"])
                print(f"Found")


        batch = self.youtube.new_batch_http_request(callback=batch_callback)

        for title in title_list:
            batch.add(self.youtube.search().list(
                part="snippet",
                maxResults=1,
                q=title,
                type="video"
            ))

        batch.execute()

        print("id_list:", id_list)
        return id_list


    def add_songs(self, song_id_list, playlist_id):
        added_id_list = []

        def batch_callback(request_id, response, exception):
            if exception is not None:
                print(exception)
            else:
                added_id_list.append(response["items"][0]["id"])
                print(f"Added")


        batch = self.youtube.new_batch_http_request(callback=batch_callback)

        for song_id in song_id_list:
            request_body = {
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                        "videoId": song_id
                    }
                }
            }

            batch.add(self.youtube.playlistItems().insert(
                part = "snippet",
                body = request_body
            ))

        batch.execute()

        return added_id_list