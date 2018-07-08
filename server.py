import socket
import sys

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
socket.bind( (sys.argv[1], int(sys.argv[2])) )

while True:
    msg, client = socket.recvfrom(1024)
    print(msg.decode(), " from: ", client)