from abc import ABC, abstractmethod

class MusicProvider(ABC):
    def __init__(self): 
        self.__access_token:str = ''

    def _set_access_token(self, access_token)->None:
        self.__access_token = access_token

    def _get_access_token(self)->str:
        return self.__access_token     
    
    
    @abstractmethod
    def set_access_token(self, access_token=None, client_id=None, client_secret=None, refresh_token=None):
        raise NotImplementedError 

    @abstractmethod
    def retrieve_playlist(self, playlist_id, out_file_path='', test_threshold=None):
        raise NotImplementedError    
