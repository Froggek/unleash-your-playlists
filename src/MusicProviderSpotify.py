from abc import get_cache_token
from typing import List
import requests
from requests.auth import HTTPBasicAuth
from requests.models import CaseInsensitiveDict
import json

from MusicProvider import MusicProvider

class MusicProviderSpotify(MusicProvider): 
    def __init__(self):
        super().__init__()

    def set_access_token(self, client_id, client_secret, refresh_token):
        """Request a refreshed access token
        See official doc: https://developer.spotify.com/documentation/general/guides/authorization/code-flow/#request-a-refreshed-access-token
        """
        basic_auth = HTTPBasicAuth(client_id, client_secret) 
        body_params = { 'grant_type': 'refresh_token', 'refresh_token': refresh_token }
        response = requests.post('https://accounts.spotify.com/api/token', auth=basic_auth, data=body_params)
        
        self._set_access_token(response.json()['access_token'])
    

    def retrieve_playlist(self, playlist_id, out_file_path='', test_threshold=None)->list:
        # Since Spotify response is paginated, we need to provide an offset + a limit 
        offset = 0
        other_tracks_to_retrieve = True
        PAGE_SIZE: int = 50 if not test_threshold else test_threshold

        request_headers = CaseInsensitiveDict() 
        request_headers['Authorization'] = f'Bearer { self._get_access_token() }'
        query_params = { 'fields': 'items(track(name).artists(name)),total', 'limit': PAGE_SIZE }
        query_path = f'https://api.spotify.com/v1/playlists/{ playlist_id }/tracks'

        tracks = list()    

        while other_tracks_to_retrieve: 
            query_params['offset'] = offset 
            response = requests.get(query_path, params=query_params, headers=request_headers)
            # TODO: check status code

            tracks += response.json()['items']
            offset += PAGE_SIZE
            other_tracks_to_retrieve = (offset < response.json()['total']) if not test_threshold else (offset < test_threshold)


        if out_file_path:
            with open(out_file_path, 'w') as f:
                f.write(json.dumps(tracks))

        return tracks



def get_access_token(client_id, client_secret, refresh_token):
    raise NotImplementedError

def retrieve_playlist(access_token, playlist_id, out_file_path='', test_threshold=None): 
    raise NotImplementedError

