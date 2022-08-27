from enum import Enum 
import os 
from google_auth_oauthlib.flow import _RedirectWSGIApp, _WSGIRequestHandler, InstalledAppFlow 
import wsgiref.simple_server 
import webbrowser


class MusicProviderName(Enum): 
    DEEZER = 0
    SPOTIFY = 1
    YOUTUBE = 2


class TokenGenerator:

    @staticmethod
    def __retrieve_config(provider):
        # TODO: change the strategy 
        PROJECT_ROOT_PATH = os.path.join(os.path.dirname(__file__), '..')

        match provider: 
            case MusicProviderName.DEEZER: 
                config_file_path = os.path.join(PROJECT_ROOT_PATH, 'data', 'config-deezer.json')
                scopes = ['basic_access', 'email']
            case MusicProviderName.SPOTIFY: 
                config_file_path = os.path.join(PROJECT_ROOT_PATH, 'data', 'config-spotify.json')
                scopes = ['user-read-private', 'user-read-email']
            case MusicProviderName.YOUTUBE:
                config_file_path = os.path.join(PROJECT_ROOT_PATH, 'data', 'config-youtube.json')
                scopes = ['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']
            case _:
                raise Exception('Unknown music provider')
        
        return config_file_path, scopes

    @staticmethod
    def execute_token_retrieval_flow(provider):
        config_file_path, scopes = TokenGenerator.__retrieve_config(provider)

        flow = InstalledAppFlow.from_client_secrets_file(
            config_file_path,
            scopes
        )

        # Reproducing the flow.run_local_server() method 
        wsgi_app = _RedirectWSGIApp("All right - 200 OK")
        local_server = wsgiref.simple_server.make_server(
            'localhost', 8080, app=wsgi_app, handler_class=_WSGIRequestHandler
        )

        flow.redirect_uri = 'http://localhost:8080/'
        auth_url, _ = flow.authorization_url()

        webbrowser.open(auth_url, new=1, autoraise=True)

        # If it doesn't work: you should browse the page... 

        local_server.handle_request()

        try:
            authorization_response = wsgi_app.last_request_uri.replace('http', 'https')
            token_request = flow.fetch_token(authorization_response=authorization_response
                , include_client_id = (provider == MusicProviderName.DEEZER)
                )
            
            # Because Deezer OAuth flow s*cks, the expiration parameter: 
            #   - Is ill-named 
            #   - Is a str, while an int is expected 
            if provider == MusicProviderName.DEEZER: 
                flow.oauth2session.token['expires_at'] = int(flow.oauth2session.token['expires'])

            # TODO: log 
            # logging.getLogger().debug(f'Got token {token_request["access_token"]} (lifetime={token_request["expires_at"]})')

            credz = flow.credentials

            # TODO: log 
            # logging.getLogger().debug(f'Credentials: {credz.to_json()}')
        
        finally: 
            local_server.server_close()

