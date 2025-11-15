import shutil
from pathlib import Path
from Config.pathes import openPlanetPath

def pluginHandler() -> None :
    ROOT = Path(__file__).resolve().parents[2]

    distantPluginFolder = openPlanetPath / "PM_GetData"
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
    else :
        print("No need for update")
    return 