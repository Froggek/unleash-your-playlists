from abc import ABC, abstractmethod
import requests
from urllib.parse import urlparse
from urllib.error import HTTPError


class MusicProvider(ABC):
    def __init__(self, domain_name, config_credentials=None): 
        self.__access_token:str = ''
        self.__DOMAIN_NAME:str = domain_name

    def _set_access_token(self, access_token)->None:
        self.__access_token = access_token

    def _get_access_token(self)->str:
        return self.__access_token     
    

    def _is_provider_specific_response_ok(self, rep:requests.Response) -> tuple[bool, str]:
        return True, ''


    # TODO: have proper logs 
    def check_response_2xx(self, rep: requests.Response, custom_error_message:str='', safe_error_codes: list=[]) -> None: 
        # There are error codes we might accept... 
        is_ok = rep.status_code in safe_error_codes
        
        if is_ok:
            #TODO: proper log 
            print(f'Got a (silented) error { rep.status_code }...OK')
        else:
            is_ok = rep.status_code in range(200, 300)
        
        std_error_msg = ''

        if not is_ok: 
            #TODO: status_code might no longer be required 
            std_error_msg = f'Code: { rep.status_code } ({ rep.reason }) - Message: { rep.text }'

        else:
            is_ok, std_error_msg = self._is_provider_specific_response_ok(rep)  

        if not is_ok: 
            print(custom_error_message if custom_error_message else 'Error!')
            raise HTTPError(url=rep.url, code=rep.status_code, msg=std_error_msg, hdrs=rep.headers, fp=None)



    @abstractmethod
    def set_access_token(self, access_token=None, client_id=None, client_secret=None, refresh_token=None):
        raise NotImplementedError 

    @abstractmethod
    def retrieve_playlist(self, playlist_id, out_file_path='', test_threshold=None)->list:
        raise NotImplementedError

    def search_tracks(self, playlist_tracks: list, output_file_path:str='')->list: 
        raise NotImplementedError

    def search_track(self, track_name: str, artist_names:str='', output_file_path:str='')->tuple:
        raise NotImplementedError 

    def add_tracks_to_playlist(self, playlist_id, tracks_ids:list=None, tracks_file_path:str=None):
        raise NotImplementedError
