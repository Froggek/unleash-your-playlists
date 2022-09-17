import threading
from xml.dom import NotFoundErr

from MusicProvider import MusicProvider
import FileHelpers

#TODO: caution - this is Deezer-specific 
class SearchThreading(threading.Thread):
    def __init__(self, music_provider: MusicProvider, playlist_tracks: list):
        threading.Thread.__init__(self)
        self.__music_provider = music_provider
        self.__playlist_tracks = playlist_tracks
        self.__output_track_ids = []

    @property
    def output_track_ids(self): 
        return self.__output_track_ids

    @output_track_ids.setter
    def output_track_ids(self, track_ids): 
        raise NotImplementedError


    def run(self):
        count:int = 0  

        for item in self.__playlist_tracks:
            track = FileHelpers.check_key_and_return_value(item, 'track')

            if 'raw' in track:
                nb_hits, id = self.__music_provider.search_track(raw_query=track['raw'])
            
            elif 'name' in track: 
                nb_hits, id = self.__music_provider.search_track(track_name=track['name'], 
                                artist_names=(' '.join(artist['name'] for artist in track['artists'])) if 'artists' in track 
                                                    else None) 
            
            else: 
                raise NotFoundErr('Either a raw query or a track\'s name is required to perform a search') 

            count += 1

            if nb_hits > 0: 
                self.output_track_ids.append(id)

            # TODO: report, print what has been found, and compare
            # TODO: use locks?   
            # Both expressions in a single "print" statement, 
            # in case the function is parallelized  
            print(f'#{ count }: { track } \n\tFound { nb_hits } match(es) - Keeping #{ id }')

        # The run method returns nothing 

