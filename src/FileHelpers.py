import os
from tabnanny import check 
import yaml 

def check_key(object, key_name):
    """Test whether `key_name` is contained in `object`
    If not, throws an exception. 
    `key_name` wan be a list, e.g. ['a', 'b', 'c']
    In that case, the method looks for object['a']['b']['c']"""

    if isinstance(key_name, list):
        keys = key_name
    else: 
        keys = [key_name]
    
    current_object = object

    for k in keys: 
        if not k in current_object:
            raise KeyError(f"The key {'>'.join(keys)} (specifically {k}) cannot be found in the object")
        
        current_object = current_object[k]


def load_config_from_file(config_folder_name='data', config_file_name='config.yaml'):
    PROJECT_ROOT_PATH = os.path.join(os.path.dirname(__file__), '..')

    with open(os.path.join(PROJECT_ROOT_PATH, config_folder_name, config_file_name), 'r') as config_file: 
        config = yaml.load(config_file, Loader=yaml.FullLoader) 
    
    check_key(config, ['output', 'temp_dir_path']) 

    TEMP_DIR_PATH = config['output']['temp_dir_path'].replace('$ROOT', PROJECT_ROOT_PATH)

    return config, TEMP_DIR_PATH

