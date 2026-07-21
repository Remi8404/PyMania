from math import radians, cos, sin
from random import randint
from pmpk.core.game_state import Coordinates
from pandas import concat, DataFrame


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

def recenterDataFrame(df:DataFrame, columns: list[str] = ["x", "y", "z"]) -> DataFrame:
    centered = df.copy()
    for col in columns:
        col_min = df[col].min()
        col_max = df[col].max()
        center = (col_min + col_max) / 2
        centered[col] = df[col] - center
    return centered
    
    
    
    
    
    
    
    