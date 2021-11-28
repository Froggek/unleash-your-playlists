import urllib.request
import requests
from requests.models import CaseInsensitiveDict


# Downhtml page 
# urllib.request.urlretrieve('https://open.spotify.com/playlist/3Rj1ranRmxL3Xy15AWMq4v?si=g2QoOdboTuyECiB0yIYEHQ&fbclid=IwAR2jgRY4sLXP3MNCXDo3xduLl-JFLUb-BzqZ7SjQXixZoKfNeNhr_BtriSc&nd=1', 'spotify.html')

my_headers = CaseInsensitiveDict(); 
my_headers['Authorization'] = 'Bearer BQC0GweM55Rpy72UqlY2SppVMXDBrUP0Ka9etNZdJzj9X7zhpTePnTTh07r9M9-ZFerdPQ6wVQO-pzpTRRCpjIx3MbIwH8c4m4ziJOE_h7jZi3F3i29djFa-Fe87QZLxY0nwxUe9qDyh9RItMo4hRYDRDtKxCld55WGhe28'

# Query API 
response = requests.get('https://api.spotify.com/v1/playlists/3Rj1ranRmxL3Xy15AWMq4v/tracks', headers=my_headers) 


print(response.json())

# print('Hello, IT!')



