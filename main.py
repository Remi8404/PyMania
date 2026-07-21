import sys
from PyQt6.QtWidgets import QApplication

from pmpk.tools.windows import Graphic3DWindow
from pmpk.geometry import drawHelicoidaleCurve, drawRandomCurve, recenterDataFrame    

def main():
    df = recenterDataFrame(drawHelicoidaleCurve(ppl=50, n_layers=4, z_dif=4), ["x","y"])
    
    app = QApplication(sys.argv)
    
    window=Graphic3DWindow(pos="up-right")
    window.show()
    window.setLine(pos=df, color=(0, 1, 0, 1))
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
