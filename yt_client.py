import os
import pickle

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request



class YTClient():
    def __init__(self):
        self.clients_secrets_file = os.getenv("CLIENT_SECRET_PATH")
        self.credentials = None
        self.youtube = self._authorize()


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
        return youtube


    def list_channels(self):
        request = self.youtube.channels().list(
            part="statistics",
            forUsername="TheHoinoel"
        )

        response = request.execute()

        print(response)


    def make_playlist(self):
        request_body = {
            "snippet": {
                "channelId": "UCeVKa9MfOuXxIkYanPukgig",
                "title": "NewPlaylistYee",
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
        
        print(response)


    def find_song(self, title):
        pass
        # return song_id


    def add_song_to_playlist(self, song_id):
        pass
