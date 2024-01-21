from abc import ABC, abstractmethod
from typing import Any
import requests 
import json 
from urllib.error import HTTPError
from MusicProviderName import MusicProviderName 
from TokenGenerator import TokenGenerator
from SearchThreaded import SearchThreading

class MusicProvider(ABC):
    def __init__(self, provider_name: MusicProviderName, config_credentials=None): 
        self.__access_token:str = ''
        self.PROVIDER_NAME: MusicProviderName = provider_name
        self.__DOMAIN_NAME:str = '' 

        match provider_name: 
            case MusicProviderName.SPOTIFY: 
                self.__DOMAIN_NAME = 'spotify.com'
            case MusicProviderName.DEEZER: 
                self.__DOMAIN_NAME = 'deezer.com'
            case MusicProviderName.YOUTUBE:
                self.__DOMAIN_NAME = 'youtube.com'
            case _: 
                raise Exception(f'The music provider "{provider_name.name}" is unknown') 

        # Retrieving an access token, or generating a new one 
        if not self._retrieve_access_token(config_credentials):
            self.__generate_access_token(config_credentials)


    def _set_access_token(self, access_token)->None:
        self.__access_token = access_token

    def _get_access_token(self)->str:
        return self.__access_token    

    def _retrieve_access_token(self, config_credentials) -> bool:
        """If an access token already exists, stores it.
        Otherwise, returns False"""
        if 'access_token' in config_credentials: 
            self.set_access_token(config_credentials['access_token'])
            return True
        
        return False

    def __generate_access_token(self, config_credentials)->None:
        if all(k in config_credentials for k in ('app_id', 'app_secret')): 
            #TODO: log using OAuth flow 
            access_token, refresh_token = TokenGenerator.execute_token_retrieval_flow(self.PROVIDER_NAME \
                , client_id=config_credentials['app_id'], client_secret=config_credentials['app_secret'])
            self.set_access_token(client_id=config_credentials['app_id'] \
                , client_secret=config_credentials['app_secret'] \
                , access_token=access_token)
            
            #TODO: remove this 
            print(self.__DOMAIN_NAME, access_token)

        else: 
            raise Exception(f'A client ID and secret are required for the "{self.PROVIDER_NAME.name}" provider')     
    

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

    def add_tracks_to_playlist(self, playlist_id, tracks_ids:list=None, tracks_file_path:str=None):
        # TODO: option to previously clear the playlist 
        raise NotImplementedError

    def search_tracks(self, playlist_tracks: list, output_file_path:str='', nb_threads=1)->list: 
        if nb_threads < 1:
            raise Exception('The number of threads must be at least 1')

        # No need to thread-ify if the playlist is small 
        ACTUAL_NB_THREADS = nb_threads if len(playlist_tracks) > nb_threads else 1
        tracks_ids = []
        
        threads = list()
        # Launching the threads

        for i in range(ACTUAL_NB_THREADS):
            threads.append(SearchThreading(playlist_tracks[i::ACTUAL_NB_THREADS], self._search_track_in_thread))
            threads[i].start()

        # Collecting the results 
        # TODO: keep order 
        for i in range(ACTUAL_NB_THREADS):
            threads[i].join()
            tracks_ids += threads[i].output_track_ids

        if (output_file_path): 
            with open(output_file_path, 'w') as f: 
                f.write(json.dumps(tracks_ids))

        return tracks_ids
    
    @abstractmethod
    def search_track(self, track_name: str='', artist_names:str='', raw_query:str='', output_file_path:str='')->tuple:
        raise NotImplementedError

    def _search_track_in_thread(self, track: dict) -> tuple:
        if 'raw' in track:
            return self.search_track(raw_query=track['raw'])

        elif 'name' in track: 
            return self.search_track(track_name=track['name'], 
                            artist_names=(' '.join(artist['name'] for artist in track['artists'])) if 'artists' in track 
                                                else None) 
        else: 
            raise KeyError('Either a raw query or a track\'s name is required to perform a search') 


from MusicProviderDeezer import MusicProviderDeezer
from MusicProviderSpotify import MusicProviderSpotify
from MusicProviderYouTube import MusicProviderYouTube

def create_provider(provider_name: str, credentials: Any) -> MusicProvider:    
    match provider_name: 
        case 'deezer': 
            return MusicProviderDeezer(credentials)
        case 'spotify':
            return MusicProviderSpotify(credentials)
        case 'youtube':
            return MusicProviderYouTube(credentials)
        case _: 
            raise KeyError(f"The music provider ${provider_name} is unknown, or not supported")