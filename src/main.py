import os
from PluginHandler.pluginHandler import pluginHandler
from Server.runServer import runServer

def main() -> None :
    os.system('cls' if os.name == 'nt' else 'clear')
    pluginHandler()
    runServer()


if __name__ == "__main__":
    main()