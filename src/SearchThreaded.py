import threading
import json 

from MusicProvider import MusicProvider

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
            track = item['track']
            track_name = track['name']
            artists = ' '.join(artist['name'] for artist in track['artists'])
            count += 1

            nb_hits, id = self.__music_provider.search_track(track_name, artists) 


            if nb_hits > 0: 
                self.output_track_ids.append(id)

            # TODO: report, print what has been found, and compare
            # TODO: use locks?   
            # Both expressions in a single "print" statement, 
            # in case the function is parallelized  
            print(f'#{ count }: { track_name } ({ artists })\n\tFound { nb_hits } match(es) - Keeping #{ id }')

        # The run method returns nothing 

