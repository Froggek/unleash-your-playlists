from array import array
import os
import yaml 

from deezer import search_track, add_tracks_to_playlist
from spotify import retrieve_playlist, get_access_token

# TODO: 
# - Error management (HTTP codes) 


if __name__ == '__main__':
    PROJECT_ROOT_PATH = os.path.join(os.path.dirname(__file__), '..')
    

    with open(os.path.join(PROJECT_ROOT_PATH, 'data', 'config.yaml'), 'r') as config_file: 
        config = yaml.load(config_file, Loader=yaml.FullLoader) 

    TEMP_DIR_PATH = config['output']['temp_dir_path'].replace('$ROOT', PROJECT_ROOT_PATH)

    spotify_credentials = config['credentials']['spotify']
    spotify_access_token = get_access_token(spotify_credentials['app_id'], spotify_credentials['app_secret'], spotify_credentials['refresh_token'])
    # TODO: check source service 
    playlist_tracks = retrieve_playlist(spotify_access_token, playlist_id=config['source']['playlist_id']\
        , out_file_path=os.path.join(TEMP_DIR_PATH, 'playlist.tmp.json')\
        # , test_threshold=100\
        ) 

    deezer_access_token = config['credentials']['deezer']['access_token']
    count:int = 0 
    deezer_tracks_ids = []

    for item in playlist_tracks:
        track = item['track']
        track_name = track['name']
        artists = ' '.join(artist['name'] for artist in track['artists'])
        count += 1
        print(f'#{count}: {track_name} ({artists})')

        nb_hits, id = search_track(config['credentials']['deezer']['access_token'], track_name, artists)
        if nb_hits > 0: 
            deezer_tracks_ids.append(id)

        # TODO: report, print what has been found, and compare 
        print(f'Found {nb_hits} match(es) - Keeping #{id}')

    if (deezer_tracks_ids): 
        # TODO: check target service 
        add_tracks_to_playlist(deezer_access_token, playlist_id=config['target']['playlist_id'], tracks_ids=deezer_tracks_ids)


    # print(count)

     

    
        
