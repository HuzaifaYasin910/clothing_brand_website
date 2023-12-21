from pathlib import Path
import json
import logging


BASE_DIR_local = Path(__file__).resolve().parent.parent
config_data = None
def load_configurations():
    json_file_path_local = BASE_DIR_local / 'credentials.json'
    global config_data
    try:
        if json_file_path_local.exists():
            with open(json_file_path_local, 'r') as config_file:
                config_data = json.load(config_file)
                
                return config_data
        else:
            absolute_file_path = Path('/home/ubuntu/credentials.json')
            if absolute_file_path.exists():
                with open(absolute_file_path, 'r') as config_file:
                    config_data = json.load(config_file)
                    return config_data
            else:
                raise FileNotFoundError("######################## Both file paths are invalid ########################")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f' Error loading configurations: {e} ')
        return None
    except Exception as e:
        logging.error(f' Unexpected error: {e} ')
        return None



