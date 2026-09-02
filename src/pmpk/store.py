from typing import Any, Callable

from pmpk.utils import SingletonMeta
from dataclasses import dataclass

class Store(metaclass=SingletonMeta):
    def __init__(self):
        print("creating store")
        self.state: dict[str, Any] = {}
        
    def getState(self, key:str):
        if key in self.state.keys():
            return self.state[key]
        else: return ""    
    
    def setState(self, key:str, value:Any):
        self.state[key] = value
      
class Context():
    def __init__(self, ts:float, logger: Callable[[str], None]):
        self.ts = ts
        self.logger = logger
        
    def log(self, text: str):
        self.logger(text)
    
    def setTS(self, ts: float):
        self.ts = ts