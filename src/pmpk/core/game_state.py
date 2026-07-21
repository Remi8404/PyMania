from pandas import DataFrame
from dataclasses import dataclass

@dataclass
class Coordinates:
    columns = ["x", "y", "z"]
    x: float
    y: float
    z: float
    def __str__(self) -> str :
        return f"[{self.x:2f}\t-\t{self.y:2f}\t-\t{self.z:2f}]"
    
    def getCSVRow(self, sep:str=",") -> str :
        return f"{self.x}{sep}{self.y}{sep}{self.z}"
    
    def getDFRow(self) -> DataFrame:
        return DataFrame(data=[[self.x, self.y, self.z]], columns=Coordinates.columns)
    
@dataclass
class Orientation:
    columns = ["yaw", "pitch", "roll"]
    yaw: float
    pitch: float
    roll: float

    def __str__(self) -> str:
        return f"Yaw : {self.yaw:2f}\nPitch : {self.pitch:2f}\nRoll : {self.roll:2f}"
    
    def getCSVRow(self, sep:str=",") -> str:
        return f"{self.yaw}{sep}{self.pitch}{sep}{self.roll}"
    
    def getDFRow(self) -> DataFrame:
        return DataFrame(data=[[self.yaw, self.pitch, self.roll]], columns=Orientation.columns)

class GameState:
    def __init__(self, **kwargs : dict[str, float|bool]):
        self.coords : Coordinates = Coordinates(kwargs["x"], kwargs["y"], kwargs["z"])
        self.orientation : Orientation = Orientation(kwargs["yaw"], kwargs["pitch"], kwargs["roll"])