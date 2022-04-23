import os
import yaml 

from deezer import search_track

if __name__ == '__main__':
    PROJECT_ROOT_PATH = os.path.join(os.path.dirname(__file__), '..')

    with open(os.path.join(PROJECT_ROOT_PATH, 'data', 'config.yaml'), 'r') as config_file: 
        config = yaml.load(config_file, Loader=yaml.FullLoader) 
        print(config)

    search_track(config['credentials']['deezer']['access_token'], 'Maryland', 'Elephanz Eugénie', 
    temp_out_file=os.path.join(*config['output']['temp_file_path'].replace('$ROOT', PROJECT_ROOT_PATH).split('/')))

    
