from typing import Any, Callable

from pmpk.utils import SingletonMeta
from typing import Any

class Store(metaclass=SingletonMeta):
    def __init__(self):
        print("Creating store ...")
        self.state: dict[str, Any] = {}
        print("Store successfully created !")
        
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
        
    def __getitem__(self, key:str):
        match key :
            case "ts":
                return self.ts
            case "logger":
                return self.logger
            case _:
                pass
            
    def __setitem__(self, key: str, value: Any):
        match key :
            case "ts":
                self.ts: float = value
            case "logger":
                self.logger: Callable[[str],None] = value
            case _:
                pass
                
    def log(self, text: str):
        self.logger(text)
        
    def update(self, **kwargs : dict[str, Any]) -> "Context":
        for key, value in kwargs.items():
            self[key] = value
        return self