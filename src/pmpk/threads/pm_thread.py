from threading import Thread, Event
from typing import Callable, Any

class PMThread(Thread):
    def __init__(self, name:str, target:Callable[[Any], None], args:tuple[Any]):
        super().__init__(name=name, target=target, args=args)
        self.stop_event = Event()
        
    def run(self):
        pass