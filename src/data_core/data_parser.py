from typing import Optional, Dict, Union, List

PositionData = Dict[str, List[float]]
ParsedPositions = Dict[str, PositionData]
ReceivedData = Dict[str, Union[float, bool, Dict[str, float]]]

def positionParser(data: ReceivedData, parsedPositions: Optional[ParsedPositions] = None) -> None:
    if parsedPositions is None:
        parsedPositions = {
            "previous": {"x": [], "y": [], "z": []},
            "current": {"x": [], "y": [], "z": []}
        }
    current_traj = parsedPositions["current"]
    is_reset_signal = data.get('startTime') == 4294967295 
    is_finished = data.get('isFinished', False)

    if is_finished or is_reset_signal:
        if current_traj["x"]:
            parsedPositions["previous"]["x"] = current_traj["x"].copy()
            parsedPositions["previous"]["y"] = current_traj["y"].copy()
            parsedPositions["previous"]["z"] = current_traj["z"].copy()
            current_traj["x"].clear()
            current_traj["y"].clear()
            current_traj["z"].clear()
        return
    
    position_data = data.get('position')
    if isinstance(position_data, dict) and 'x' in position_data and 'y' in position_data and 'z' in position_data:
        current_traj["x"].append(position_data['x'])
        current_traj["y"].append(position_data['y'])
        current_traj["z"].append(position_data['z'])
    return