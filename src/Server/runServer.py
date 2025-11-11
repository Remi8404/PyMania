import socket
import struct

def runServer() -> None :
    HOST = '127.0.0.1'
    PORT = 9000
    PACKET_SIZE = 13  
    FORMAT = '<fffB' 

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    print(f"Server is listening on {HOST}:{PORT}...")

    while True:
        try:
            conn, addr = server_socket.accept() 
            print(f"✅ Connection established from {addr}")

            with conn:
                while True:
                    data = conn.recv(PACKET_SIZE)
                    
                    if not data:
                        print("Connection closed by client (OpenPlanet).")
                        break
                    
                    if len(data) == PACKET_SIZE:
                        speed, accel, jerk, is_finished_byte = struct.unpack(FORMAT, data)
                        is_finished = bool(is_finished_byte)

                        print(f"Speed: {speed:.2f}, Accel: {accel:.2f}, Jerk: {jerk:.2f}, Finished: {is_finished}")
                    else:
                        print(f"Received incomplete data (expected {PACKET_SIZE} bytes, got {len(data)}). Disconnecting.")
                        break
        
        except socket.error as e:
            print(f"Socket error: {e}. Restarting listener...")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            if 'conn' in locals() and conn is not None:
                conn.close()