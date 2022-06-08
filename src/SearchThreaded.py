import threading
from MusicProvider import MusicProvider

class SearchThreading(threading.Thread):
    def __init__(self, music_provider: MusicProvider, playlist_tracks: list):
        threading.Thread.__init__(self)
        self.music_provider = music_provider
        self.playlist_tracks = playlist_tracks
        
    def run(self):
        self.music_provider.search_tracks(self.playlist_tracks, '')

