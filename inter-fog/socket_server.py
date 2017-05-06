# Echo client program
import socket
import time
import os
import sys

snode = "/tmp/ffsocket.sock"

try:
    if os.path.exists(snode):
        os.remove(snode)
except OSError:
    print(str(OSError))

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
#s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(snode)
print("Listen on socket: {0}".format(snode))
s.listen(1)
conn, addr = s.accept()
print("Accepted connection with")

while True:
    try:
        data = conn.recv(1024)
        print("Received: {0}".format(str(data)))
        conn.send(data)
    except KeyboardInterrupt:
        conn.close()
        print ("Connection closed")
        sys.exit()
