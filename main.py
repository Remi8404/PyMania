import sys
from PyQt6.QtWidgets import QApplication

from pmpk.graphics.windows import Graphic3DWindow, ConsoleWindow
from pmpk.geometry import drawHelicoidaleCurve, drawRandomCurve, recenterDataFrame
from pmpk.graphics.commands import build_registry    

def main():
    df = recenterDataFrame(drawHelicoidaleCurve(ppl=50, n_layers=4, z_dif=4), ["x","y"])
    
    app = QApplication(sys.argv)
    
    console=ConsoleWindow(build_registry())
    console.show()
    
    window=Graphic3DWindow(pos="up-right")
    window.show()
    
    window.setLine(pos=df, color=(0, 1, 0, 1))
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
