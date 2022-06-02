from math import floor
import requests, os, yaml 
import json 
import helpers

from MusicProvider import MusicProvider

class MusicProviderDeezer(MusicProvider):
    def set_access_token(self, access_token=None, client_id=None, client_secret=None, refresh_token=None):
        # TODO
        if not access_token:
            raise Exception('Access token is required')

        self._set_access_token(access_token) 
    

    def __search_track(self, track_name: str, artist_names:str='', temp_out_file:str='')->tuple: 
        query_params = { 'access_token': self._get_access_token() }

        # TODO: Sanity check 
        # response = requests.get('https://api.deezer.com/user/me', params=query_params)
        # print(response.json())

        # Performing a Deezer "Advanced Search"
        # https://developers.deezer.com/api/search 
        # query_params['q'] = 'artist:"Elephanz Eugénie" track:"Maryland"'
        query_params['q'] = (f'artist:"{ artist_names }"' if artist_names else '') + f'track:"{ track_name }"'
        # Hopefully retrieving the most relevant tracks first 
        query_params['order'] = 'RANKING'

        response = requests.get('https://api.deezer.com/search', params=query_params)

        # Loging result 
        if (temp_out_file): 
            with open(temp_out_file, 'w') as f:
                f.write(response.text)

        # Handling codes != 2xx 
        if not helpers.is_response_2xx(response, f'Error when searching for a Deezer track: { track_name } ({ artist_names })'): 
            return 0, None 
        
        response_json = response.json() 

        return response_json['total'], (response_json['data'][0]['id'] if response_json['data'] else None)


    def search_tracks(self, playlist_tracks: list, output_file_path:str='')->list: 
        deezer_tracks_ids = []
        count:int = 0  

        for item in playlist_tracks:
            track = item['track']
            track_name = track['name']
            artists = ' '.join(artist['name'] for artist in track['artists'])
            count += 1
            print(f'#{ count }: { track_name } ({ artists })')

            nb_hits, id = self.__search_track(track_name, artists)
            if nb_hits > 0: 
                deezer_tracks_ids.append(id)

            # TODO: report, print what has been found, and compare 
            print(f'Found { nb_hits } match(es) - Keeping #{ id }')

        if (output_file_path): 
            with open(output_file_path, 'w') as f: 
                f.write(json.dumps(deezer_tracks_ids))

        return deezer_tracks_ids
        

    def __add_tracks_to_playlist(self, playlist_id: str, tracks_ids: list):
        # TODO: option to previously clear the playlist 

        query_params = { 'access_token': self._get_access_token() }
        # Thank you steinitzu 
        # https://github.com/steinitzu/pydeezer/blob/master/pydeezer/__init__.py 
        # The songs must be provided as a QUERY parameter (serialized array)  

        tracks_set = set([ t for t in tracks_ids])
        tracks_duplicates = [ t for t in tracks_ids if tracks_ids.count(t) > 1 ]
        if tracks_duplicates: 
            print(f'The following track # have been duplicated from the source: ')
            for t in tracks_duplicates: 
                print(f"\t# {t}")
            
         # We check what the target playlist already contains
        target_playlist_track_ids = self.retrieve_playlist(playlist_id) 
        tracks_already_in_target = set([t for t in tracks_set if t in target_playlist_track_ids])

        if tracks_already_in_target:
            print(f'The following track # were already in the target playlist: ')
            for t in tracks_already_in_target:
                print(f'\t# {t}')
        
        # Removing tracks already in target 
        tracks_set = tracks_set - tracks_already_in_target

        for t in tracks_set:
            if t in target_playlist_track_ids:
                tracks_set.remove(t)

        if not tracks_set:
            print('No track to add...END')
            return

        # TODO maxQueryString = 1024 characters 
        query_params['songs'] = ','.join(str(track) for track in tracks_set) 
        response = requests.post(f'https://api.deezer.com/playlist/{ playlist_id }/tracks', params=query_params)
        helpers.is_response_2xx(response, f'Error while adding tracks: {query_params["songs"]}')


    def add_tracks_to_playlist(self, playlist_id, tracks_ids:list=None, tracks_file_path:str=None):
        if not tracks_ids:  
            if tracks_file_path: 
                with open(tracks_file_path) as f: 
                    tracks_ids = json.loads(f.read())
            else: 
                raise Exception('Either a list of tracks or a track file path are required')

        return self.__add_tracks_to_playlist(playlist_id, tracks_ids)


    def retrieve_playlist(self, playlist_id, out_file_path='', test_threshold=None) -> list:
        query_params = { 'access_token': self._get_access_token() }

        response = requests.get(f'https://api.deezer.com/playlist/{ playlist_id }', params=query_params)
        
        if not helpers.is_response_2xx(response, f'Error while retrieving playlist Deezer # { playlist_id }'): 
            raise Exception(f'Error while retrieving playlist Deezer # { playlist_id }')

        response_tracks = response.json()
            
        if not ('tracks' in response_tracks and 'data' in response_tracks['tracks'] and isinstance(response_tracks['tracks']['data'], list)):
            f'Error while retrieving playlist Deezer # { playlist_id }'
        
        response_tracks = response_tracks['tracks']['data']

        return [item['id'] for item in response_tracks]




# TODO... 
def get_access_token(): 
    """ This function is not ready yet... """

    PROJECT_ROOT_PATH = os.path.join(os.path.dirname(__file__), '..')
    with open(os.path.join(PROJECT_ROOT_PATH, 'data', 'config.yaml'), 'r') as config_file: 
      config = yaml.load(config_file, Loader=yaml.FullLoader)
    deezer = config['credentials']['deezer'] 

    # See https://developers.deezer.com/api/oauth & https://developers.deezer.com/myapps (app's page)
    # "manage_library" scope is required to manage the playlists
    # Note: when a NEW scope is required, add on at the TOP of the list
    query_params = { 'app_id': deezer['app_id'], 'secret': deezer['app_secret'], 'redirect_uri': deezer['app_redirect_uri'], \
        'perms': 'basic_access,email,manage_library,offline_access' }
    # "offline_access" is needed 
    response = requests.get('https://connect.deezer.com/oauth/auth.php', params=query_params)
    print(response.request.url)
    # => Code: abcd... 

    query_params = { 'app_id': '$APP_ID', 'secret': '$APP_SECRET', 'code': '$CODE' } 
    # https://connect.deezer.com/oauth/access_token.php
    # => Access token: xxx-xxx-xxx-xxx 
    # response = requests.get('https://connect.deezer.com/oauth/access_token.php', params=query_params) 
    # print(response.json())
    







