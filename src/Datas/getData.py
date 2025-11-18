import socket
import struct

PACKET_SIZE = 45  
FORMAT = '<fffffffffBBBBIB' 

def getData(conn: socket.socket):
    formattedData: dict[str, float | bool | dict[str, bool | float]] = {}
    socketData = conn.recv(PACKET_SIZE)
    
    if not socketData:
        print("Connection closed by client (OpenPlanet).")
        formattedData["connectionClose"] = True
        return formattedData
    
    if len(socketData) == PACKET_SIZE:
        speed, accel, sideSpeed, yaw, pitch, roll, x, y, z, flGroundContact, frGroundContact, rlGroundContact, rrGroundContact, startTime, isFinishedByte = struct.unpack(FORMAT, socketData)
        formattedData['speed'] = speed
        formattedData['acceleration'] = accel
        formattedData['sideSpeed'] = sideSpeed
        formattedData['yaw'] = yaw
        formattedData['pitch'] = pitch
        formattedData['roll'] = roll
        formattedData['position'] = {
            "x":x,
            "y":y,
            "z":z
        }
        formattedData['wheelsState'] = {
            "FL":bool(flGroundContact),
            "FR":bool(frGroundContact),
            "RL":bool(rlGroundContact),
            "RR":bool(rrGroundContact)
            }
        formattedData['startTime'] = startTime
        formattedData['isFinished'] = bool(isFinishedByte)
        
        return formattedData
    else:
        print(f"Received incomplete data (expected {PACKET_SIZE} bytes, got {len(socketData)}). Disconnecting.")
        formattedData["connectionClose"] = True
        return formattedData