from array import array
import os
import yaml 

from MusicProviderDeezer import MusicProviderDeezer, search_tracks
from MusicProviderSpotify import MusicProviderSpotify

# TODO: 
# - Error management (HTTP codes) 


if __name__ == '__main__':
    PROJECT_ROOT_PATH = os.path.join(os.path.dirname(__file__), '..')
    
    with open(os.path.join(PROJECT_ROOT_PATH, 'data', 'config.yaml'), 'r') as config_file: 
        config = yaml.load(config_file, Loader=yaml.FullLoader) 

    TEMP_DIR_PATH = config['output']['temp_dir_path'].replace('$ROOT', PROJECT_ROOT_PATH)


    spotify:MusicProviderSpotify = MusicProviderSpotify()
    spotify_credentials = config['credentials']['spotify']
    # TODO: have this in ctor 
    spotify.set_access_token(client_id=spotify_credentials['app_id'], client_secret=spotify_credentials['app_secret']\
        , refresh_token=spotify_credentials['refresh_token'])

    deezer:MusicProviderDeezer = MusicProviderDeezer()
    deezer.set_access_token(access_token=config['credentials']['deezer']['access_token'])

    # TODO: check source service 
    playlist_tracks = spotify.retrieve_playlist(playlist_id=config['source']['playlist_id']\
        , out_file_path=os.path.join(TEMP_DIR_PATH, 'playlist.tmp.json')\
        # , test_threshold=100\
        ) 

    # TODO 
    if (False): 
        deezer_tracks_ids = search_tracks(deezer_access_token, playlist_tracks\
            , output_file_path=os.path.join(TEMP_DIR_PATH, 'deezer_tracks_to_add.tmp.json')\
            )

        # TODO: support empty lists 
        if (deezer_tracks_ids): 
            # TODO: check target service 
            add_tracks_to_playlist_from_list_ids(deezer_access_token, playlist_id=config['target']['playlist_id'], tracks_ids=deezer_tracks_ids)
    else: 
        deezer.add_tracks_to_playlist(playlist_id=config['target']['playlist_id']\
            , tracks_file_path=os.path.join(TEMP_DIR_PATH, 'deezer_tracks_to_add.tmp.json')\
            )


