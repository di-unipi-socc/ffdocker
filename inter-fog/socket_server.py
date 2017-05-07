# Echo client program
import socket
import time
import os
import sys

snode = "/tmp/ffsocket1.sock"

try:
    if os.path.exists(snode):
        os.remove(snode)
except OSError as e:
    print(e)
    sys.exit()

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

s.bind(snode)
print("Listen on socket: {0}".format(snode))
s.listen(1)

#wait to accept a connection - blocking call
conn, addr = s.accept()
print("Accepted connection")

while True:
    try:
        data = conn.recv(1024)
        print("Received: {0}".format(data.decode("utf-8")))
        conn.send(data)
    except KeyboardInterrupt:
        conn.close()
        print ("Connection closed")
        sys.exit()
