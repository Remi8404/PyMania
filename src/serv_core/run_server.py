import socket
from time import sleep

HOST = '127.0.0.1'
PORT = 9000

def runServer() -> socket.socket:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((HOST, PORT))
    serverSocket.listen(1)
 
    print(f"\tServer is listening on {HOST}:{PORT}...")
    print("\tWaiting for a connection from OpenPlanet...")
    try:
        conn, addr = serverSocket.accept() 
        print(f"Connection established from {addr}")
        return conn                                      
    except socket.error as e:
        print(f"Socket error: {e}. Restarting listener in 5 seconds...")
        sleep(5)
        return runServer()
    except Exception as e:
        print(f"An unexpected error occurred: {e}. Restarting listener in 5 seconds...")
        sleep(5)
        return runServer()
    
