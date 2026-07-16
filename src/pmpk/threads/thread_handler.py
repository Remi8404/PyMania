from threading import Thread
from pm_thread import PMThread
from typing import Callable, Any

class ThreadHandler : 
    """
    A class designed to oversee every Thread started in a project.
    """
    def __init__(self):
        self.threads : dict[str, PMThread] = {}
    
    def startThread(self, name:str, function:Callable[[Any], None], params:tuple[Any] = (), is_daemon:bool = False) -> None:
        """
        Starts a thread and store it in its thread container.
        Args:
            name (str): The identifier used to handle the thread.
            function (callable): The function that must be runned as a thread. 
            params (tuple): provide all arguments that must be supplied to the function (by default, none)
            is_daemon (bool): If all threads that are running are daemons, then the program will stop.
        Returns:
            None
        """
        if name in self.threads.keys() and self.threads[name].is_alive():
            print(f"A thread nammed {name} is already running. Kill this thread or change the provided name to proceed.")
            return
        new_thread = PMThread(target=function, name=name, args=params)
        new_thread.daemon = is_daemon
        new_thread.start()
        self.threads[name] = new_thread
        print(f"Thread {name} has been successfully started ! ")
        return
    
    def killThread(self, name:str):
        """
        Kill a thread based on its name. Raise the Stop Event to True and properly stop it when the run function has stopped.
        Args:
            name (str): the name given to the thread which must be shut down.
        Returns:
            None
        """
        if name in self.threads.keys() and self.threads[name].is_alive():
            self.threads[name].stop_event.set()
            self.threads[name].join()
        return
    
    def killAllThreads(self):
        """
        Kill all living threads in its threads store.
        """
        for thread in self.threads.values() :
            if thread.is_alive() :
                thread.stop_event.set()
                thread.join()
        return
    
    def __del__(self):
        self.killAllThreads()
        return