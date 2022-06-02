from abc import ABC, abstractmethod
from xml import dom
import requests
from urllib.parse import urlparse


class MusicProvider(ABC):
    def __init__(self, domain_name): 
        self.__access_token:str = ''
        self.__DOMAIN_NAME:str = domain_name

    def _set_access_token(self, access_token)->None:
        self.__access_token = access_token

    def _get_access_token(self)->str:
        return self.__access_token     
    

    def _is_provider_specific_response_ok(self, rep:requests.Response) -> tuple[bool, str]:
        return True, ''


    # TODO: have proper logs 
    def check_response_2xx(self, rep: requests.Response, custom_error_message:str='') -> None: 
        is_ok = rep.status_code in range(200, 300)
        std_error_msg = ''

        if not is_ok: 
            std_error_msg = f'Code: { rep.status_code } ({ rep.reason }) - Message: { rep.text }'

        else:
            is_ok, std_error_msg = self._is_provider_specific_response_ok(rep)  

        if not is_ok: 
            print(custom_error_message if custom_error_message else 'Error!')
            raise Exception(std_error_msg)



    @abstractmethod
    def set_access_token(self, access_token=None, client_id=None, client_secret=None, refresh_token=None):
        raise NotImplementedError 

    @abstractmethod
    def retrieve_playlist(self, playlist_id, out_file_path='', test_threshold=None)->list:
        raise NotImplementedError

    def search_tracks(self, playlist_tracks: list, output_file_path:str='')->list: 
        raise NotImplementedError

    def add_tracks_to_playlist(self, playlist_id, tracks_ids:list=None, tracks_file_path:str=None):
        raise NotImplementedError
