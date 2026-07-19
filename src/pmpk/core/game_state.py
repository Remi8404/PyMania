from pandas import DataFrame

class Coordinates:
    columns = ["x", "y", "z"]
    
    def __init__(self, x:float, y: float, z:float):
        self.x = x
        self.y = y
        self.z = z
        
    def __str__(self) -> str :
        return f"[{self.x:2f}\t-\t{self.y:2f}\t-\t{self.z:2f}]"
    
    def getCSVRow(self, sep:str=",") -> str :
        return f"{self.x}{sep}{self.y}{sep}{self.z}"
    
    def getDFRow(self) -> DataFrame:
        return DataFrame(data=[[self.x, self.y, self.z]], columns=self.columns)
        

class GameState:
    def __init__(self):
        self.coords : Coordinates