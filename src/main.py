import os
from venv import create
import FileHelpers 
import logging
from MusicProvider import MusicProvider 

from MusicProviderDeezer import MusicProviderDeezer
from MusicProviderSpotify import MusicProviderSpotify
from MusicProviderYouTube import MusicProviderYouTube
from MusicProvider import create_provider

if __name__ == '__main__':    
    logging.basicConfig(level=logging.INFO) 

    config, TEMP_DIR_PATH = FileHelpers.load_config_from_file()

    FileHelpers.check_key_and_return_value(config, ['source', 'playlist_id'])
    FileHelpers.check_key_and_return_value(config, ['source', 'service'])
    FileHelpers.check_key_and_return_value(config, ['target', 'playlist_id'])
    FileHelpers.check_key_and_return_value(config, ['target', 'service'])
    source_service, target_service = config['source']['service'], config['target']['service']
    # FileHelpers.check_key_and_return_value(config, ['credentials', 'spotify'])
    FileHelpers.check_key_and_return_value(config, ['credentials', 'deezer'])
    FileHelpers.check_key_and_return_value(config, ['credentials', 'youtube'])
    
    # spotify:MusicProviderSpotify = MusicProviderSpotify(config['credentials']['spotify'])
    # deezer:MusicProviderDeezer = MusicProviderDeezer(config['credentials']['deezer'])
    # youtube:MusicProviderYouTube = MusicProviderYouTube(config['credentials']['youtube'])

    source_provider = create_provider(source_service, config['credentials'][source_service])
    target_provider = create_provider(target_service, config['credentials'][target_service])

    # TODO: check source service 
    # playlist_tracks = spotify.retrieve_playlist(playlist_id=config['source']['playlist_id']\
    #    , out_file_path=os.path.join(TEMP_DIR_PATH, 'playlist.tmp.json')\
    #    # , test_threshold=100\
    #    ) 
    

    playlist_tracks = source_provider.retrieve_playlist(playlist_id=config['source']['playlist_id']\
        , out_file_path=os.path.join(TEMP_DIR_PATH, 'output_source_tracks.tmp.json')\
        # , test_threshold=100\
        ) 

    _ = target_provider.search_tracks(playlist_tracks\
        , output_file_path=os.path.join(TEMP_DIR_PATH, 'output_target_found_tracks.tmp.json')\
        , nb_threads=8
        )
    target_provider.add_tracks_to_playlist(playlist_id=config['target']['playlist_id']\
        , tracks_file_path=os.path.join(TEMP_DIR_PATH, 'output_target_found_tracks.tmp.json')\
        )


