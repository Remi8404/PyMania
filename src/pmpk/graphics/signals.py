from PyQt6.QtCore import QObject, pyqtSignal

class Signals(QObject):
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if Signals._instance:
            return Signals._instance
        else: return Signals()
    
    def __init__(self):
        if Signals._instance:
            return Signals._instance
        self.consoleSignal = pyqtSignal(str)
        
    