import threading
import FileHelpers
from collections.abc import Callable 

class SearchThreading(threading.Thread):
    """
        Helper to parallelize the search queries across various music providers 
    """

    def __init__(self, playlist_tracks: list, search_track_fn: Callable[[dict], tuple]):
        threading.Thread.__init__(self)
        self.__playlist_tracks = playlist_tracks
        self.__output_track_ids = []
        self.__search_track_fn = search_track_fn

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
            nb_hits, id = self.__search_track_fn(track)

            count += 1

            if nb_hits > 0: 
                self.output_track_ids.append(id)

            # TODO: report, print what has been found, and compare
            # TODO: use locks?   
            # Both expressions in a single "print" statement, 
            # in case the function is parallelized  
            print(f'#{ count }: { track } \n\tFound { nb_hits } match(es) - Keeping #{ id }')

        # The run method returns nothing 

