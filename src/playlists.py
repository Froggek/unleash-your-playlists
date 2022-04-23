import requests
from requests.models import CaseInsensitiveDict


my_headers = CaseInsensitiveDict() 
# TODO: get token as input 
# my_headers['Authorization'] = f'Bearer {...}'

query_params = { 'fields': 'items(track(name).artists(name))' }

# Query API 
response = requests.get('https://api.spotify.com/v1/playlists/3Rj1ranRmxL3Xy15AWMq4v/tracks', params= query_params, headers=my_headers) 


print(response.json())




# print('Hello, IT!')



