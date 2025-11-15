import json
import os

DEFAULT_FILE = 'default_config.json'
LOCAL_FILE = 'local_config.json'

script_dir = os.path.dirname(os.path.abspath(__file__))

default_path = os.path.join(script_dir, DEFAULT_FILE)
local_path = os.path.join(script_dir, LOCAL_FILE)

def configHandler() -> dict[str, str]:
    try:
        with open(default_path, 'r') as f:
            default_config = json.load(f)
    except FileNotFoundError:
        print(f"Error : File '{DEFAULT_FILE}' not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: File '{DEFAULT_FILE}' is not a valid JSON.")
        return {}

    config = default_config.copy() 
    
    if os.path.exists(local_path):
        try:
            with open(local_path, 'r') as f:
                local_config = json.load(f)
            config.update(local_config)
            print(f"Configuration set to '{LOCAL_FILE}'.")
            
        except json.JSONDecodeError:
            print(f"Warning : '{LOCAL_FILE}' corrupted or empty. Using default values.")

    else:
        print(f"Error : File '{LOCAL_FILE}' not found. Default values used instead")
            
    return config


def set_config_value(key: str, value):
    if os.path.exists(local_path):
        try:
            with open(local_path, 'r') as f:
                local_config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            local_config = {}
    else:
        local_config = {}
    local_config[key] = value
    try:
        with open(local_path, 'w') as f:
            json.dump(local_config, f, indent=4) 
        print(f"\nValue of '{key}' updated in {LOCAL_FILE}.")
    except Exception as e:
        print(f"\nError while writing in {LOCAL_FILE}: {e}")


