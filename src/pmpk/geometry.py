from math import radians, cos, sin
from random import randint
from pmpk.core.game_state import Coordinates
from pandas import read_csv, concat, DataFrame

from pathlib import Path
from os.path import isfile

from typing import Literal
from datetime import datetime


def drawHelicoidaleCurve(radius:float = 10, ppl:int = 20, n_layers:int = 1, z_dif:int =10) -> DataFrame :
    """
    Creates an array of coordinates that corresponds to an helicoidale curve
    Args:
        radius (float): Radius of base circle.
        ppl (int): Points Per Layer. Corresponds to the number of point a circle should have
        n_layers (int): How many full circles should be drawn. 
        z_dif (int): The difference on the Z axis between the first point of a circle and its last. 
    Returns:
        None
    """
    z = n_layers*z_dif
    delta_z = z_dif/ppl
    
    theta = 0
    delta_theta = radians(360/ppl)
    df = DataFrame(columns=Coordinates.columns)
    
    for _ in range(n_layers):
        for _ in range(ppl):
            df = concat([df, Coordinates(radius*cos(theta), radius*sin(theta), z).getDFRow()])
            theta += delta_theta
            z -= delta_z
            
    return df

def drawRandomCurve(n_points:int = 400):
    df = DataFrame(columns=Coordinates.columns)
    x = randint(0,200)
    y = randint(0, 200)
    z = randint(0, 100)
    for _ in range(n_points):
        df = concat([df, Coordinates(x,y,z).getDFRow()])
        x += randint(-5,20)/15
        y += randint(-5,20)/15
        z += randint(-5,2)/10
    return df

def writeFileFromCurve(df:DataFrame, run_folder: str, extension: str, naming_method:Literal["specified", "date"]="date", f_name:str = "") -> None:
    match naming_method:
        case "specified":
            rel_path = run_folder / Path(f"{f_name}.{extension}")
            print(rel_path)
        case "date":
            rel_path = run_folder / Path(f"{datetime.today().strftime("%Y%m%d_%H%M%S")}")
    df.to_csv(rel_path, index=False)

def getCurveFromFile(run_folder: Path, f_name:str, extension:str)-> DataFrame :
    rel_path = run_folder / Path(f"{f_name}.{extension}")
    if isfile(rel_path):
        df = read_csv(rel_path)
        return df
    else: 
        print(f"{rel_path} is not an actual file.")
        return DataFrame(columns=Coordinates.columns)

def recenterDataFrame(df:DataFrame, columns: list[str] = ["x", "y", "z"]) -> DataFrame:
    centered = df.copy()
    for col in columns:
        col_min = df[col].min()
        col_max = df[col].max()
        center = (col_min + col_max) / 2
        centered[col] = df[col] - center
    return centered
    
    
    
    
    
    
    
    