from PluginHandler.pluginHandler import pluginHandler
from Server.runServer import runServer

def main() -> None :
    pluginHandler()
    runServer()


if __name__ == "__main__":
    main()