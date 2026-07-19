from cmd import Cmd
from pmpk.threads.thread_handler import ThreadHandler

class PMCmd(Cmd):
    intro = 'Welcome to PyMania CMD. Type help or ? to list commands.\n'
    prompt = 'PyMania >> '
    file = None
    handler = ThreadHandler()
    
    def do_quickstart(self) -> None:
        return
        
    def do_quit(self) -> None :
        self.handler.killAllThreads()
        del self.handler
        return
    
    