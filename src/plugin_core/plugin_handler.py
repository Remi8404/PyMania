import shutil
from pathlib import Path
from src.config_core.config_handler import configHandler

def pluginHandler() -> None :
    config = configHandler()
    ROOT = Path(__file__).resolve().parents[2]

    if config['openplanetPath'] == "" :
        print("Invalid Path, Plugin can't be updated automatically.\n\tEither specify a correct path in Config/local_config.py or copy it manually.\n\n")
        return

    distantPluginFolder = Path(config["openplanetPath"]) / "PM_GetData"
    distantPluginFile = distantPluginFolder / "main.as"
    distantPluginUpdate = distantPluginFile.stat().st_mtime if distantPluginFolder.exists() else 0

    localPluginFolder = ROOT / "PM_GetData"
    localPluginFile= localPluginFolder / "main.as"
    localPluginUpdate = localPluginFile.stat().st_mtime
    
    if localPluginUpdate > distantPluginUpdate :
        print("Moving local plugin to OpenplanetNext Plugins folder ...")
        if distantPluginFolder.exists():
            shutil.rmtree(distantPluginFolder)
        shutil.copytree(localPluginFolder, distantPluginFolder)
        print("PM_GetData update successed !")
    else :
        print("No need to update PM_GetData")
    return 