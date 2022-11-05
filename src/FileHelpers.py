import os
from typing import Any 
import yaml 

def check_key_and_return_value(object: Any, key: str | list)->Any:
    """TL; DR; Test whether `key` can be found in `object`
    If not, throws an exception. 

    `key` can be a list, e.g. ['a', 'b', 'c']
    In that case, the method looks for object['a']['b']['c']
    
    Details: If `key` is of type str, then `object` is assumed to be a dict
        If so, `object`[`key`] is returned 

    If `key` if of type int, the type of `object` is checked: 
        - If dict, behavior is unchanged
        - If list or tuple, we check whether the length of `object` > `key`
            (if so, the `key`th element is returned) 
    """

    if isinstance(key, list):
        keys = key
    elif isinstance(key, tuple):
        keys = list(key) 
    else: # a 1-level key
        keys = [key]
    
    current_object = object

    for k in keys: 
        match k: 
            case str() | float():
                if not k in current_object:
                    raise KeyError(f"The key {'>'.join(keys)} (specifically { k }) cannot be found in the object")
            case int():
                if (isinstance(current_object, list) or isinstance(current_object, tuple)) and (k >= len(current_object)): 
                    raise KeyError(f"The {'>'.join(keys)}th element cannot be retrieved from the object, \
                        since the list/tuple only contains { len(current_object) } element(s)") 
            case _:
                raise KeyError(f'The (sub-)key { k } is of type { type(k) }, \
                    which is not supported')

        current_object = current_object[k]

    return current_object

def load_config_from_file(config_folder_name='data', config_file_name='config.yaml'):
    PROJECT_ROOT_PATH = os.path.join(os.path.dirname(__file__), '..')

    with open(os.path.join(PROJECT_ROOT_PATH, config_folder_name, config_file_name), 'r') as config_file: 
        config = yaml.load(config_file, Loader=yaml.FullLoader) 
    
    check_key_and_return_value(config, ['output', 'temp_dir_path']) 

    TEMP_DIR_PATH = config['output']['temp_dir_path'].replace('$ROOT', PROJECT_ROOT_PATH)

    return config, TEMP_DIR_PATH

