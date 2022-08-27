from array import array
import os
import yaml 

from MusicProviderDeezer import MusicProviderDeezer
from MusicProviderSpotify import MusicProviderSpotify
from SearchThreaded import SearchThreading

if __name__ == '__main__':
    PROJECT_ROOT_PATH = os.path.join(os.path.dirname(__file__), '..')
    
    with open(os.path.join(PROJECT_ROOT_PATH, 'data', 'config.yaml'), 'r') as config_file: 
        config = yaml.load(config_file, Loader=yaml.FullLoader) 

    TEMP_DIR_PATH = config['output']['temp_dir_path'].replace('$ROOT', PROJECT_ROOT_PATH)


    if ('credentials' not in config) or ('spotify' not in config['credentials']):
            raise Exception('The credentials are not available for the provider "Spotify" in the configuration file')

    spotify_credentials = config['credentials']['spotify']
    spotify:MusicProviderSpotify = MusicProviderSpotify('spotify.com', spotify_credentials)
    
    deezer:MusicProviderDeezer = MusicProviderDeezer('deezer.com')
    deezer.set_access_token(access_token=config['credentials']['deezer']['access_token'])

    # TODO: check source service 
    playlist_tracks = spotify.retrieve_playlist(playlist_id=config['source']['playlist_id']\
        , out_file_path=os.path.join(TEMP_DIR_PATH, 'playlist.tmp.json')\
        # , test_threshold=100\
        ) 

    # TODO 
    deezer_tracks_ids = deezer.search_tracks(playlist_tracks\
        , output_file_path=os.path.join(TEMP_DIR_PATH, 'deezer_tracks_to_add.tmp.json')\
        , nb_threads=8
        )
    deezer.add_tracks_to_playlist(playlist_id=config['target']['playlist_id']\
        , tracks_file_path=os.path.join(TEMP_DIR_PATH, 'deezer_tracks_to_add.tmp.json')\
        )


