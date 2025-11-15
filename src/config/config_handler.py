
from Config.default_config import config as defaultConfig
from Config.local_config import config as localConfig

def configHandler() :
    config: dict[str, str] = {}
    defaultKeys: set[str] = defaultConfig.keys()
    localKeys: set[str]  = localConfig.keys()
    for key in defaultKeys : 
        if key in localKeys :
            config[key] = localConfig[key]
        else :
            config[key] = defaultConfig[key]
    return config
     
