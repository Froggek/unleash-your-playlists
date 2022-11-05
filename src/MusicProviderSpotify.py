import requests
# from requests.auth import HTTPBasicAuth
from requests.models import CaseInsensitiveDict
import json
from MusicProviderName import MusicProviderName
from MusicProvider import MusicProvider

class MusicProviderSpotify(MusicProvider): 
    def __init__(self, config_credentials=None):
        super().__init__(MusicProviderName.SPOTIFY, config_credentials)
        
    # TODO: support refresh tokens 
    # def _retrieve_access_token(self, config_credentials) -> bool:
    #     """If an access token is available, stores it. 
    #     Else, if a refresh token is available, a new access token is geerated ans stored
    #     Otherwise, returns False"""

    #     if super()._retrieve_access_token(self, config_credentials):
    #         return True

    #     if all(k in config_credentials for k in ('app_id', 'app_secret', 'refresh_token')): 
    #         # TODO: log refresh token used 
    #         # TODO: check scopes? 
    #         self.set_access_token(client_id=config_credentials['app_id']\
    #             , client_secret=config_credentials['app_secret']\
    #             , refresh_token=config_credentials['refresh_token'])
    #         return True 
        
    #     return False


    def set_access_token(self, access_token=None, client_id=None, client_secret=None, refresh_token=None):
        if not access_token:
            raise Exception('Access token is required')

        self._set_access_token(access_token) 

    # TODO: support refresh tokens 
    # def set_access_token(self, access_token=None, client_id=None, client_secret=None, refresh_token=None):
    #     """If provided, set an access token. 
    #     Otherwise, request one from the provided refresh token.  
    #     See official doc: https://developer.spotify.com/documentation/general/guides/authorization/code-flow/#request-a-refreshed-access-token
    #     """
    #     if access_token: 
    #         self._set_access_token(access_token)
        
    #     else: # requests a new fresh access token  
    #         if not refresh_token:
    #             raise Exception('Refresh token is required')

    #         basic_auth = HTTPBasicAuth(client_id, client_secret) 
    #         body_params = { 'grant_type': 'refresh_token', 'refresh_token': refresh_token }
    #         response = requests.post('https://accounts.spotify.com/api/token', auth=basic_auth, data=body_params)
    #         # TODO: check response code 
    #         # TODO check scopes 
    #         self._set_access_token(response.json()['access_token'])
        

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
            self.check_response_2xx(response, 'Error while retrieving the playlist') 

            tracks += response.json()['items']
            offset += PAGE_SIZE
            other_tracks_to_retrieve = (offset < response.json()['total']) if not test_threshold else (offset < test_threshold)


        if out_file_path:
            with open(out_file_path, 'w') as f:
                f.write(json.dumps(tracks))

        return tracks

    def search_track(self, track_name: str = '', artist_names: str = '', raw_query: str = '', output_file_path: str = '') -> tuple:
        raise NotImplementedError

