# Echo client program
import socket
import time
import os
import sys
import pickle



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

print("FNC - Accepted connection ...")
conn, addr = s.accept()
state = 0
while state < 5:
    # wait to accept a connection - blocking call
    try:
        data = pickle.loads(conn.recv(1024))
        print("Received: {0}".format(data))
        if data['state'] == 5:
            conn.send(pickle.dumps({"action":"migrate"}))
            data = pickle.loads(conn.recv(1024))
            if data["migrate"] == "yes":
                print("Migrating Container")
                time.sleep(3)
        else:
            conn.send(pickle.dumps({"action":"nothing"}))

    except KeyboardInterrupt:
        conn.close()
        print ("Connection closed")
        sys.exit()

conn.send(pickle.dumps({"op":"state"}))
