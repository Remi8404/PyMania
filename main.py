import sys
from PyQt6.QtWidgets import QApplication

from pmpk.graphics.windows import Graphic3DWindow, ConsoleWindow
from pmpk.geometry import drawHelicoidaleCurve, drawRandomCurve, recenterDataFrame
from pmpk.graphics.commands import build_registry    
from pmpk.store import Store

def main():
    
    app = QApplication(sys.argv)
    
    console=ConsoleWindow(build_registry())
    console.show()
    
    graphic=Graphic3DWindow(pos="up-right")
    graphic.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
