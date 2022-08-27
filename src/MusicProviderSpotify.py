import requests
from requests.auth import HTTPBasicAuth
from requests.models import CaseInsensitiveDict
import json

from MusicProvider import MusicProvider

class MusicProviderSpotify(MusicProvider): 
    def __init__(self, domain_name, config_credentials):
        super().__init__(domain_name, config_credentials)

        if all(k in config_credentials for k in ('app_id', 'app_secret', 'refresh_token')): 
            self.set_access_token(client_id=config_credentials['app_id']\
                , client_secret=config_credentials['app_secret']\
                , refresh_token=config_credentials['refresh_token'])

        else: 
            raise Exception('Refresh token not available for Spotify provider')


    def set_access_token(self, access_token=None, client_id=None, client_secret=None, refresh_token=None):
        """Request a refreshed access token
        See official doc: https://developer.spotify.com/documentation/general/guides/authorization/code-flow/#request-a-refreshed-access-token
        """

        # TODO 
        if not refresh_token:
            raise Exception('Refresh token is required')

        basic_auth = HTTPBasicAuth(client_id, client_secret) 
        body_params = { 'grant_type': 'refresh_token', 'refresh_token': refresh_token }
        response = requests.post('https://accounts.spotify.com/api/token', auth=basic_auth, data=body_params)
        

        # TODO check scopes 
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

