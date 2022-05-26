import requests
from urllib.parse import urlparse

# TODO: have proper logs 
def is_response_2xx(rep: requests.Response, custom_error_message:str='') -> bool: 
    is_ok = rep.status_code in range(200, 300)
    std_error_msg = ''

    if not is_ok: 
        std_error_msg = f'Code: {rep.status_code} ({rep.reason}) - Message: {rep.text}'

    elif urlparse(rep.request.url).netloc.endswith('deezer.com'):
        is_ok, std_error_msg = is_deezer_response_ok(rep)  


    if not is_ok: 
        print(custom_error_message if custom_error_message else 'Error!')
        print(std_error_msg)

    return is_ok


# TODO: move to a Deezer class
# TODO: might not be serializable in json  
def is_deezer_response_ok(rep:requests.Response) -> tuple[bool, str]:
    """Deezer-specific errors are detailed here: https://developers.deezer.com/api/errors"""

    # A single boolean can be returned if the request succeeds 
    if isinstance(rep.json(), dict) and 'error' in rep.json():
        deezer_error = rep.json()['error'] 
        return False, f'Code: {deezer_error["code"]} ({deezer_error["type"]}) - Message: {deezer_error["message"]}'
    
    return True, ''

