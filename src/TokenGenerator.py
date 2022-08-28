from google_auth_oauthlib.flow import _RedirectWSGIApp, _WSGIRequestHandler, InstalledAppFlow 
import wsgiref.simple_server 
import webbrowser
from MusicProviderName import MusicProviderName


class TokenGenerator:

    @classmethod
    def __retrieve_config(cls, provider, client_id, client_secret):
        # TODO: change the strategy 
        # PROJECT_ROOT_PATH = os.path.join(os.path.dirname(__file__), '..')
        # config_file_path = os.path.join(PROJECT_ROOT_PATH, 'data', f'config-{provider.name.lower()}.json')

        oauth_config = {
            'installed': {
                'client_id': client_id,
                'client_secret': client_secret,
                # TODO?  
                # 'redirect_uris': ['http://localhost', 'urn:ietf:wg:oauth:2.0:oob'],
                # 'auth_uri': '', 
                # 'token_uri': ''
            }
        }

        match provider: 
            case MusicProviderName.DEEZER: 
                oauth_config['installed']['scopes'] = ['basic_access', 'email']
                oauth_config['installed']['auth_uri'] = 'https://connect.deezer.com/oauth/auth.php'
                oauth_config['installed']['token_uri'] = 'https://connect.deezer.com/oauth/access_token.php'
            case MusicProviderName.SPOTIFY: 
                oauth_config['installed']['scopes'] = ['user-read-private', 'user-read-email']
                oauth_config['installed']['auth_uri'] = 'https://accounts.spotify.com/authorize'
                oauth_config['installed']['token_uri'] = 'https://accounts.spotify.com/api/token'
            case MusicProviderName.YOUTUBE:
                oauth_config['installed']['scopes'] = ['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']
            case _:
                raise Exception('Unknown music provider')
        
        return oauth_config

    @classmethod
    def execute_token_retrieval_flow(cls, provider, client_id, client_secret, ):
        oauth_config = cls.__retrieve_config(provider, client_id, client_secret)

        flow = InstalledAppFlow.from_client_config(oauth_config, oauth_config['installed']['scopes'] \
            #, **kwargs
            )

        # flow = InstalledAppFlow.from_client_secrets_file(
        #     config_file_path,
        #     scopes
        # )
        LOCAL_SERVER_PORT = '808' + str(provider.value)

        # Reproducing the flow.run_local_server() method 
        wsgi_app = _RedirectWSGIApp("All right - 200 OK")
        local_server = wsgiref.simple_server.make_server(
            'localhost', int(LOCAL_SERVER_PORT), app=wsgi_app, handler_class=_WSGIRequestHandler
        )

        flow.redirect_uri = f'http://localhost:{LOCAL_SERVER_PORT}/'
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

            # credz = flow.credentials

            # TODO: log 
            # logging.getLogger().debug(f'Credentials: {credz.to_json()}')
        
        finally: 
            local_server.server_close()

        return flow.credentials.token, flow.credentials.refresh_token
