import requests
# from requests.models import CaseInsensitiveDict

def get_access_token(): 
    """ This function is not ready yet... """

    # See https://developers.deezer.com/api/oauth & https://developers.deezer.com/myapps (app's page)
    query_params = { 'app_id': '$APP_ID', 'secret': '$APP_SECRET', 'redirect_uri': '$REDIRECT_URI', 'perms': 'basic_access,email,offline_access' }
    # "offline_access" is needed 
    # response = requests.get('https://connect.deezer.com/oauth/auth.php', params=query_params)
    # print(response.json())
    # => Code: abcd... 

    query_params = { 'app_id': '$APP_ID', 'secret': '$APP_SECRET', 'code': '$CODE' } 
    # https://connect.deezer.com/oauth/access_token.php
    # => Access token: xxx-xxx-xxx-xxx 
    # response = requests.get('https://connect.deezer.com/oauth/access_token.php', params=query_params) 
    # print(response.json())


def search_track(access_token, track_name, artist_names='', temp_out_file=''): 

    query_params = { 'access_token': access_token }

    # Sanity check - TODO 
    # response = requests.get('https://api.deezer.com/user/me', params=query_params)
    # print(response.json())

    # Performing a Deezer "Advanced Search"
    # https://developers.deezer.com/api/search 
    # query_params['q'] = 'artist:"Elephanz Eugénie" track:"Maryland"'
    query_params['q'] = (f'artist:"{artist_names}"' if artist_names else '') + f'track:"{track_name}"'
    # Hopefully retrieving the most relevant tracks first 
    query_params['order'] = 'RANKING'

    response = requests.get('https://api.deezer.com/search', params=query_params)

    if (temp_out_file): 
        with open(temp_out_file, 'w') as f:
            f.write(response.text)
    
    response_json = response.json() 

    return response_json['total'], (response_json['data'][0]['id'] if response_json['data'] else None)



