from math import floor
import requests, os, yaml 
import json 
import helpers

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


# if __name__ == "__main__":
#     get_access_token()

def search_tracks(access_token, playlist_tracks, output_file_path=''): 
    deezer_tracks_ids = []
    count:int = 0  

    for item in playlist_tracks:
        track = item['track']
        track_name = track['name']
        artists = ' '.join(artist['name'] for artist in track['artists'])
        count += 1
        print(f'#{count}: {track_name} ({artists})')

        nb_hits, id = search_track(access_token, track_name, artists)
        if nb_hits > 0: 
            deezer_tracks_ids.append(id)

        # TODO: report, print what has been found, and compare 
        print(f'Found {nb_hits} match(es) - Keeping #{id}')

    if (output_file_path): 
        with open(output_file_path, 'w') as f: 
            f.write(json.dumps(deezer_tracks_ids))

    return deezer_tracks_ids
    
def search_track(access_token, track_name, artist_names='', temp_out_file=''): 

    query_params = { 'access_token': access_token }

    # Sanity check - TODO 
    # response = requests.get('https://api.deezer.com/user/me', params=query_params)
    # print(response.json())

    # Performing a Deezer "Advanced Search"
    # https://developers.deezer.com/api/search 
    # query_params['q'] = 'artist:"Elephanz Eugénie" track:"Maryland"'
    query_params['q'] = (f'artist:"{artist_names}"' if artist_names else '') + f'track:"{track_name}"'
    # Hopefully retrieving the most relevant tracks first 
    query_params['order'] = 'RANKING'

    response = requests.get('https://api.deezer.com/search', params=query_params)

    # Loging result 
    if (temp_out_file): 
        with open(temp_out_file, 'w') as f:
            f.write(response.text)

    # Handling codes != 2xx 
    if not helpers.is_response_2xx(response, f'Error when searching for a Deezer track: {track_name} ({artist_names})'): 
        return 0, None 
    
    response_json = response.json() 

    return response_json['total'], (response_json['data'][0]['id'] if response_json['data'] else None)

def add_tracks_to_playlist_from_list_ids(access_token, playlist_id, tracks_ids):
    return add_tracks_to_playlist(access_token, playlist_id, tracks_ids)

def add_tracks_to_playlist_from_file(access_token, playlist_id, tracks_file_path):
    with open(tracks_file_path) as f: 
        tracks_ids = json.loads(f.read())
    return add_tracks_to_playlist(access_token, playlist_id, tracks_ids)

def add_tracks_to_playlist(access_token, playlist_id, tracks_ids):
    # TODO: option to previously clear the playlist 
    # TODO: or check what's already in the target playlist 

    query_params = { 'access_token': access_token }
    # Thank you steinitzu 
    # https://github.com/steinitzu/pydeezer/blob/master/pydeezer/__init__.py 
    # The songs must be provided as a QUERY parameter (serialized array)  
    
    # TODO masQueryString = 1024 characters 
    pivot = floor(len(tracks_ids) / 2)

    query_params['songs'] = ','.join(str(track) for track in tracks_ids[:pivot]) 
    response = requests.post(f'https://api.deezer.com/playlist/{playlist_id}/tracks', params=query_params)
    helpers.is_response_2xx(response, f'1-Error while adding tracks: {query_params["songs"]}')

    query_params['songs'] = ','.join(str(track) for track in tracks_ids[pivot:]) 
    response = requests.post(f'https://api.deezer.com/playlist/{playlist_id}/tracks', params=query_params)
    helpers.is_response_2xx(response, f'2-Error while adding tracks: {query_params["songs"]}')

