# Echo client program
import socket
import time
import sys

snode = "/tmp/ffsocket1.sock"

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect(snode)
print("Connected to {0}".format(snode))
#time.sleep(2)
i = 0
while True:
    try:
        s.send(bytes(str(i),"utf-8"))#str(i),"UTF8"))
        print('Send: {0} '.format(str(i)))
        resp = s.recv(1024)
        time.sleep(1)
        i += 1
    except socket.error:
        s.close()
        print("Socket closed")
        sys.exit()
    except KeyboardInterrupt:
        s.close()
        print ("Socket closed")
        sys.exit()
