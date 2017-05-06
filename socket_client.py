# Echo client program
import socket
import time
import sys

snode = "/tmp/ffsocket.sock"

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect(snode)

i = 0
while True:
    try:
        s.send(bytes(i))
        print('Send: {0} '.format(str(i)))
        resp = s.recv(1024)
        time.sleep(1)
        i += 1
    except socket.error:
        s.close()
        print("Socket closed")
        sys.exit()
