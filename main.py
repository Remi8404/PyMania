import sys
from pmpk.geometry import drawHelicoidaleCurve
import pyqtgraph.opengl as gl
from PyQt6.QtWidgets import QApplication

def main():
    df = drawHelicoidaleCurve(ppc=50, n_layers=4, z_dif=4)
    app = QApplication(sys.argv)
    view = gl.GLViewWidget()
    view.show()
    grid = gl.GLGridItem()
    view.addItem(grid)
    line = gl.GLLinePlotItem(pos=df, color=(0,1,0,1), width=0.5, antialias=True, mode='line_strip')
    view.addItem(line)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
