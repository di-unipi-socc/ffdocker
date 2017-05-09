# Echo client program
import socket
import time
import sys

HOST = 'localhost'   # Symbolic name, meaning all available interfaces
PORT = 8888


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print("Connected to {0}{1}".format(HOST,PORT))
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
