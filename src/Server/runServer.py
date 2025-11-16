import socket
import struct
import os

HOST = '127.0.0.1'
PORT = 9000
PACKET_SIZE = 9  
FORMAT = '<ffB' 

def runServer() -> None :
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((HOST, PORT))
    serverSocket.listen(1)
    oldDataSet = {}
    dataSet = {}
 
    print(f"Server is listening on {HOST}:{PORT}...")

    while True:
        try:
            conn, addr = serverSocket.accept() 
            print(f"Connection established from {addr}")

            with conn:
                while True:
                    oldDataSet = dataSet.copy()
                    dataSet = getData(conn)
                    if(dataSet["connectionClose"]): break
                    if(dataSet != oldDataSet):
                        print(f"Speed: {dataSet['speed']:.2f}, Accel: {dataSet['acceleration']:.2f}, Finished: {dataSet['isFinished']}")
        
        except socket.error as e:
            print(f"Socket error: {e}. Restarting listener...")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            if 'conn' in locals() and conn is not None:
                conn.close()


def getData(conn: socket.socket):
    formattedData: dict[str, float | bool] = {"connectionClose":False}
    socketData = conn.recv(PACKET_SIZE)
    
    if not socketData:
        print("Connection closed by client (OpenPlanet).")
        return {"connectionClose":True}
    
    if len(socketData) == PACKET_SIZE:
        speed, accel, isFinishedByte = struct.unpack(FORMAT, socketData)
        isFinished = bool(isFinishedByte)
        formattedData['speed'] = speed
        formattedData['acceleration'] = accel
        formattedData['isFinished'] = isFinished
        
        return formattedData
    else:
        print(f"Received incomplete data (expected {PACKET_SIZE} bytes, got {len(socketData)}). Disconnecting.")
        return {"connectionClose":True}