import os
import FileHelpers 

from MusicProvider import MusicProviderName
from MusicProviderDeezer import MusicProviderDeezer
from MusicProviderSpotify import MusicProviderSpotify
from SearchThreaded import SearchThreading


if __name__ == '__main__':    
    config, TEMP_DIR_PATH = FileHelpers.load_config_from_file()

    FileHelpers.check_key(config, ['source', 'playlist_id'])
    FileHelpers.check_key(config, ['target', 'playlist_id'])
    FileHelpers.check_key(config, ['credentials', 'spotify'])
    FileHelpers.check_key(config, ['credentials', 'deezer'])
    
    spotify_credentials = config['credentials']['spotify']
    spotify:MusicProviderSpotify = MusicProviderSpotify(spotify_credentials)
    
    deezer_credentials = config['credentials']['deezer']
    deezer:MusicProviderDeezer = MusicProviderDeezer(deezer_credentials)

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


