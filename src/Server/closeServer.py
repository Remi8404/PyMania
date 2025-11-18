from socket import socket

def closeServer(conn: socket):
    if 'conn' in locals():
        conn.close()