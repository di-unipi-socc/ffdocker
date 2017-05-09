# Echo client program
import socket
import time
import os
import sys



HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
    print("FNC - bind on {0}:{1}".format(HOST,PORT))
except socket.error as msg:
    print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()
s.listen(1)
print("FNC - listen 1 ")

# wait to accept a connection - blocking call
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
