import shutil
from pathlib import Path

def pluginUpdate(config: dict[str, str] = {}) -> None :
    ROOT = Path(__file__).resolve().parents[2]

    if config['opp'] == "" :
        print("\tInvalid Path, Plugin can't be updated automatically.\n\tEither specify a correct path in Config/local_config.py or copy it manually.\n")
        return

    distantPluginFolder = Path(config["opp"]) / "PM_GetData"
    distantPluginFile = distantPluginFolder / "main.as"
    distantPluginUpdate = distantPluginFile.stat().st_mtime if distantPluginFolder.exists() else 0

    localPluginFolder = ROOT / "PM_GetData"
    localPluginFile= localPluginFolder / "main.as"
    localPluginUpdate = localPluginFile.stat().st_mtime
    
    if localPluginUpdate > distantPluginUpdate :
        print("\tMoving local plugin to OpenplanetNext Plugins folder ...")
        if distantPluginFolder.exists():
            shutil.rmtree(distantPluginFolder)
        shutil.copytree(localPluginFolder, distantPluginFolder)
        print("\tPM_GetData update successed !")
    else :
        print("\tNo need to update PM_GetData")
    return 