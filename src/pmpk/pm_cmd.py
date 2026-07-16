from cmd import Cmd
from threads import ThreadHandler

class PMCmd(Cmd):
    intro = 'Welcome to PyMania CMD. Type help or ? to list commands.\n'
    prompt = 'PyMania >> '
    file = ''
    
    def do_quickstart(self) -> ThreadHandler: 
        handler = ThreadHandler()
        return handler
    
    def do_quit(self) -> None :
        return
    
    