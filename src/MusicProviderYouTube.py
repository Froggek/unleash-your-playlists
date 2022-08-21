from MusicProvider import MusicProvider

class MusicProviderYouTube(MusicProvider):
    
    def set_access_token(self, access_token=None, client_id=None, client_secret=None, refresh_token=None):
        """ 
            Access and refresh tokens can be retrieved from the OAuth playground
            https://developers.google.com/oauthplayground 
        """
        
        if not refresh_token: 
            raise Exception("Refresh token is required")
        
        


