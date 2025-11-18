import os
from PluginHandler.pluginHandler import pluginHandler
from Server.runServer import runServer
from Datas.generator import generator
from Datas.runParser import positionParser


def main() -> None :
    os.system('cls' if os.name == 'nt' else 'clear')
    pluginHandler()
    conn = runServer()
    parsedPositions : dict[str, dict[str, list[float]]] = {
            "previous": {"x": [], "y": [], "z": []},
            "current": {"x": [], "y": [], "z": []}
        }
    for dataSet in generator(conn):
        positionParser(dataSet, parsedPositions)
        print(parsedPositions)

if __name__ == "__main__":
    main()