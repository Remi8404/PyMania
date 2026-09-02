from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QCompleter
from PyQt6.QtGui import QCursor
from pyqtgraph import Vector # type: ignore
import pyqtgraph.opengl as gl # type: ignore

from typing import Literal, Callable, cast

from pandas import DataFrame
import numpy as np
import time

from pmpk.graphics.commands import CommandRegistry
from pmpk.store import Store, Context

PLACEMENT:dict[str, Callable[[int, int, int, int], tuple[int, int, int, int]]] = {
    "up-left": lambda x,y,w,h : (x,y,w,h),
    "up-right" : lambda x,y,w,h : (x+w,y,w,h),
    "down-left": lambda x,y,w,h : (x,y+h,w,h),
    "down-right": lambda x,y,w,h : (x+w,y+h,w,h)
}

def getScreen(app: QApplication, method:Literal["first","cursor","size"]):    
    match method:
        case "first":
            return app.primaryScreen()
        case "cursor":
            return app.screenAt(QCursor.pos())
        case "size":
            screens = app.screens()
            for s in screens:
                print(s.availableGeometry())
            return max(screens, key=lambda s : (g := s.availableGeometry()).width() * g.height())
        case _ :
            pass

class PMWindow:
    app = None
    
    def __init__(self, name:str, target_screen:Literal["first","cursor","size"]="cursor", pos:Literal["up-left","up-right","down-left","down-right"]="up-left"):
        if PMWindow.app is None:
            PMWindow.app = cast(QApplication, QApplication.instance())
            if not PMWindow.app : 
                raise RuntimeError("You must create a QApplication before creating Windows.")
            
        screenGeometry = getScreen(PMWindow.app, target_screen).availableGeometry() # type: ignore
        screen_w, screen_h = screenGeometry.width(), screenGeometry.height()
        win_w, win_h = screen_w // 2, screen_h // 2
            
        self.window = QMainWindow()
        self.window.setWindowTitle(f"PyMania - {name}")
        self.window.setGeometry(*PLACEMENT[pos](screenGeometry.x(), screenGeometry.y(), win_w, win_h))
        
    def show(self)->None:
        self.window.show()
        
    
class Graphic3DWindow(PMWindow):
    def __init__(self, name:str="3DCurve", target_screen:Literal["first","cursor","size"]="cursor", pos:Literal["up-left","up-right","down-left","down-right"]="up-right"):
        super().__init__(name, target_screen, pos)
        
        self.center = QWidget()
        
        self.layout = QVBoxLayout(self.center)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.window.setCentralWidget(self.center)
        
        self.view = gl.GLViewWidget()
        self.layout.addWidget(self.view) 
        
        self.grid = gl.GLGridItem()
        self.view.addItem(self.grid) # type: ignore
        
        self.line3d = gl.GLLinePlotItem(pos=None, color=(0,1,0,1), width=0.5, antialias=True, mode='line_strip')
        self.view.addItem(self.line3d) # type: ignore
        Store().setState("win_g", self)
        
    def fitGridToData(self, points: np.ndarray, spacing_ratio: float = 0.1):
        points = np.asarray(points)
        mins = points.min(axis=0)
        maxs = points.max(axis=0)
        size = maxs - mins

        self.grid.setSize(x=size[0], y=size[1], z=size[2]) # type: ignore
        self.grid.setSpacing( # type: ignore
            x=size[0] * spacing_ratio,
            y=size[1] * spacing_ratio,
            z=size[2] * spacing_ratio,
        )
        
    def fitCameraToData(self, points:np.ndarray, elevation:int=30, azimuth:int=45):
        points = np.asarray(points)
        mins = points.min(axis=0)
        maxs = points.max(axis=0)
        center = (mins + maxs) / 2
        extent = np.linalg.norm(maxs - mins)
        self.view.setCameraPosition( # type: ignore
            pos=Vector(*center),
            distance=extent * 1.2,
            elevation=elevation,
            azimuth=azimuth,
        )
        
    def setLine(self, pos:tuple[int, int, int]|DataFrame, color:tuple[int, int, int, int]|DataFrame, width:float=0.5, antialias:bool=True, mode:Literal["lines","line_strip"]="line_strip", fit_camera:bool=True, fit_grid:bool=True):
        try: 
            self.line3d.setData(pos=pos, color=color, width=width, antialias=antialias, mode=mode)# type: ignore
            if fit_camera:
                self.fitCameraToData(cast(np.ndarray, pos))
            if fit_grid:
                self.fitGridToData(cast(np.ndarray, pos))
        except: 
            pass


class ConsoleWindow(PMWindow):
    def __init__(self, registry: CommandRegistry, name:str="Console", target_screen:Literal["first","cursor","size"]="cursor", pos:Literal["up-left","up-right","down-left","down-right"]="down-right"):
        super().__init__(name, target_screen, pos)
        self.registry = registry
        
        widget = QWidget()
        
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)

        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setStyleSheet("background-color: black; color: #00FF00; font-family: Consolas;")
        self.output_area.append("PyMania Cmd >> Type help to get commands list.")

        self.input_line = QLineEdit()
        self.input_line.setStyleSheet("background-color: #222; color: white; font-family: Consolas;")
        self.input_line.setPlaceholderText("Enter a command here ...")

        layout.addWidget(self.output_area)
        layout.addWidget(self.input_line)

        self.input_line.returnPressed.connect(self.process_command) # type: ignore
        
        self.window.setCentralWidget(widget)
        Store().setState("win_c", self)
        
    def print_to_console(self, text: str):
        self.output_area.append(text)
        scrollbar = self.output_area.verticalScrollBar()
        assert scrollbar is not None
        scrollbar.setValue(scrollbar.maximum())

    def process_command(self):
        raw_input = self.input_line.text().strip()
        self.input_line.clear()
        if not raw_input:
            return
        
        self.print_to_console(f"> {raw_input}")
        result = self.registry.execute(
            raw_input, 
            Context(time.perf_counter(), self.print_to_console)
        )

        if result == "__CLEAR__":
            self.output_area.clear()
        elif result:
            self.print_to_console(result)