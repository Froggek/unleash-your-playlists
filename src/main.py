import os
import FileHelpers 

from MusicProviderDeezer import MusicProviderDeezer
from MusicProviderSpotify import MusicProviderSpotify
from MusicProviderYouTube import MusicProviderYouTube
from SearchThreaded import SearchThreading


if __name__ == '__main__':    
    config, TEMP_DIR_PATH = FileHelpers.load_config_from_file()

    FileHelpers.check_key(config, ['source', 'playlist_id'])
    FileHelpers.check_key(config, ['target', 'playlist_id'])
    FileHelpers.check_key(config, ['credentials', 'spotify'])
    FileHelpers.check_key(config, ['credentials', 'deezer'])
    FileHelpers.check_key(config, ['credentials', 'youtube'])
    
    spotify:MusicProviderSpotify = MusicProviderSpotify(config['credentials']['spotify'])
    deezer:MusicProviderDeezer = MusicProviderDeezer(config['credentials']['deezer'])
    youtube:MusicProviderYouTube = MusicProviderYouTube(config['credentials']['youtube'])

    # TODO: check source service 
    # playlist_tracks = spotify.retrieve_playlist(playlist_id=config['source']['playlist_id']\
    #    , out_file_path=os.path.join(TEMP_DIR_PATH, 'playlist.tmp.json')\
    #    # , test_threshold=100\
    #    ) 
    playlist_tracks = youtube.retrieve_playlist(playlist_id=config['source']['playlist_id']\
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


