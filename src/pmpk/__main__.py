import sys
from PyQt6.QtWidgets import QApplication

from pmpk.graphics.windows import Graphic3DWindow, ConsoleWindow
from pmpk.graphics.commands import build_registry  
from pmpk.utils import EnvHandler
from pmpk.store import Store


def pmpk_start(env_handler:bool=True, store:bool=True, create_app:bool=True, console:bool=True, curve:bool=True, register_window:bool = True)->None:
    if env_handler:
        EnvHandler()
        
    if store:
        Store()
        
    if create_app:
        app = QApplication(sys.argv)
        
        if console:
            win_c=ConsoleWindow(build_registry())
            win_c.show()
            Store().setState("win_c", win_c)
        if curve:
            win_g=Graphic3DWindow(pos="up-right")
            win_g.show()    
            Store().setState("win_g", win_g)
            
        sys.exit(app.exec())
        
    
        
    