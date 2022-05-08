import os
import yaml 

from deezer import search_track
from spotify import retrieve_playlist, get_access_token

# TODO: 
# - Error management (HTTP codes) 


if __name__ == '__main__':
    PROJECT_ROOT_PATH = os.path.join(os.path.dirname(__file__), '..')
    

    with open(os.path.join(PROJECT_ROOT_PATH, 'data', 'config.yaml'), 'r') as config_file: 
        config = yaml.load(config_file, Loader=yaml.FullLoader) 

    TEMP_DIR_PATH = config['output']['temp_dir_path'].replace('$ROOT', PROJECT_ROOT_PATH)

    spotify_credentials = config['credentials']['spotify']
    access_token = get_access_token(spotify_credentials['app_id'], spotify_credentials['app_secret'], spotify_credentials['refresh_token'])
    playlist_tracks = retrieve_playlist(access_token, playlist_id='3Rj1ranRmxL3Xy15AWMq4v'\
        , out_file_path=os.path.join(TEMP_DIR_PATH, 'playlist.tmp.json')\
        ) 

    # count:int = 0 
    # for item in playlist_tracks:
    #     track = item['track']
    #     count += 1
    #     print(track['name'], end='')
    #     for artist in track['artists']: 
    #         print('-' + artist['name'], end='')
    #     if count % 50 == 0: 
    #         print('========================================================')
    #     else: 
    #         print ('')

    # print(count)

    search_track(config['credentials']['deezer']['access_token'], 'Maryland', 'Elephanz Eugénie'\
        , temp_out_file=os.path.join(TEMP_DIR_PATH, 'found_track.tmp.json')) 

    
        
