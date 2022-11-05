import requests
from requests.structures import CaseInsensitiveDict
import re 

import FileHelpers 
from MusicProvider import MusicProvider
from MusicProviderName import MusicProviderName

class MusicProviderYouTube(MusicProvider):
    def __init__(self, config_credentials=None):
        super().__init__(MusicProviderName.YOUTUBE, config_credentials)

    #TODO: be ready to deal with that error message
    #     "message": "YouTube Data API v3 has not been used in project 152162623880 before or it is disabled. 
    #      Enable it by visiting https://console.developers.google.com/apis/api/youtube.googleapis.com/overview?project=152162623880 
    #           then retry. 
    #       If you enabled this API recently, wait a few minutes for the action to propagate to our systems and retry.",
 

    def set_access_token(self, access_token=None, client_id=None, client_secret=None, refresh_token=None):
        """ 
            Access and refresh tokens can be retrieved from the OAuth playground
            https://developers.google.com/oauthplayground 
        """
        if access_token:
            self._set_access_token(access_token)        
        else: 
            raise Exception("Access token is required")

    #TODO: use the Python client 
    #TODO: implement refresh token 

    def retrieve_playlist(self, playlist_id, out_file_path='', test_threshold=None) -> list:
        """Retrieve the items from a YouTube playlist
        See https://developers.google.com/youtube/v3/docs/playlistItems/list 
        """
        PAGE_SIZE: int = 50 if (not test_threshold or test_threshold > 50) else test_threshold

        request_headers = CaseInsensitiveDict()
        # TODO: mutualize w/ Spotify 
        request_headers['Authorization'] = f"Bearer {self._get_access_token()}"
        request_headers['Accept'] = 'application/json'

        query_params = { 'part': 'snippet', 'maxResults': PAGE_SIZE, 'playlistId': playlist_id }
        query_path = f'https://youtube.googleapis.com/youtube/v3/playlistItems'

        response = requests.get(url=query_path, params=query_params, headers=request_headers)
        self.check_response_2xx(response, f'Error while retrieving the playlist "{playlist_id}" from {self.PROVIDER_NAME.name}')
        response_items = FileHelpers.check_key_and_return_value(response.json(), 'items')
        

        #TODO: set and serialize to a standard format with the other providers 
        tracks = list()

        for item in response_items:
            # Heuristic: seems like removing the '(Official Music Video)' from the title helps the subsequent search 
            # Heuristic: seems like, with YouTube as the source, we achieve better results while performing a "raw" query, 
            #               instead of looking for a track's name and an artist   
            # tracks.append({ 
            #     'track': {
            #         'name': re.sub('\(?official +((music) +)?video\)?', '', 
            #                     FileHelpers.check_key_and_return_value(item, ['snippet', 'title']), 
            #                     flags=re.IGNORECASE), 
            #         # Heuristic: seems like videoOwnerChannelTitle contains an artist's name 
            #         # Heuristic: seems loke removing the '(Official Music Video)' from the title helps the subsequent search 
            #         'artists': [ 
            #                 { 'name': item['snippet']['videoOwnerChannelTitle'], } 
            #             ]
            #         }
            #     })
            tracks.append({
                'track': {
                    'raw': re.sub('\(?official +((music) +)?video\)?', '', 
                                FileHelpers.check_key_and_return_value(item, ['snippet', 'title']), 
                                flags=re.IGNORECASE)
                }
            })

        print(tracks)
        return tracks

        #TODO: pagination (pageToken...) 

    def search_track(self, track_name: str = '', artist_names: str = '', raw_query: str = '', output_file_path: str = '') -> tuple:
        return super().search_track(track_name, artist_names, raw_query, output_file_path)


