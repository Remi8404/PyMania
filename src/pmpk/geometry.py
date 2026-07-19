from math import radians, cos, sin
from pmpk.core.game_state import Coordinates
from pandas import concat, DataFrame


def drawHelicoidaleCurve(radius:float = 10, ppc:int = 20, n_layers:int = 1, z_dif:int =10) -> DataFrame :
    """
    Creates an array of coordinates that corresponds to an helicoidale curve
    Args:
        radius (float): Radius of base circle.
        ppc (int): Points Per Circle. Corresponds to the number of point a circle should have
        n_layers (int): How many full circles should be drawn. 
        z_dif (int): The difference on the Z axis between the first point of a circle and its last. 
    Returns:
        None
    """
    z = n_layers*z_dif
    delta_z = z_dif/ppc
    
    theta = 0
    delta_theta = radians(360/ppc)
    df = DataFrame(columns=Coordinates.columns)
    
    for _ in range(n_layers):
        for _ in range(ppc):
            df = concat([df, Coordinates(radius*cos(theta), radius*sin(theta), z).getDFRow()])
            theta += delta_theta
            z -= delta_z
            
    return df
    
    
    
    
    
    
    
    