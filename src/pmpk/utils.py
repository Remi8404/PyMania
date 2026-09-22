from dotenv import load_dotenv
import os

class SingletonMeta(type):
    _instances: dict[type, object] = {}

    def __call__(cls, *args, **kwargs): # type: ignore
        if cls not in cls._instances: # type: ignore
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
    
class EnvHandler(metaclass=SingletonMeta):
    def __init__(self) -> None:
        print("Reading Env File ...")
        load_dotenv()
        print("Env successfully read !")
        
    def getVar(self, var_name:str) -> str:
        try :
            return os.environ[var_name]
        except :
            print(f"An error has occured while trying to access '{var_name}' ENV var.")
            return ""
    
    def getEnv(self):
        return dict(os.environ)
    
    