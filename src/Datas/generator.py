from Datas.getData import getData
from socket import socket

def generator(conn: socket):
    while True:
        data = getData(conn)
        yield data