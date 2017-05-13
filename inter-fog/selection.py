# Echo client program
import socket
import time
import os
import sys
import pickle
import subprocess
#server side (does not migratd y FNC)

HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.setblocking(False)

#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
    print("Selection - bind on {0}:{1}".format(HOST,PORT))
except socket.error as msg:
    print ('Selection - Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()
s.listen(1)

print("Selection - Accepted connection ...")
conn, addr = s.accept()

#s.setblocking(0)  # non blocking socket when it is connected

received = 0
while True:
    # wait to accept a connection - blocking call
    print("waiting receic...")
    try:
        data = pickle.loads(conn.recv(1024))
        print("Selection - Received {0}".format(data))
        received +1
        #if data['state'] == 5:
        #conn.send(pickle.dumps({"action":"migrate"}))
        #data = pickle.loads(conn.recv(1024))
        #print("Selection - Received {0}".format(data))
            # if data["migrate"] == "yes":
            #     cid = data['id']
            #     print("FNC - Migrating Container {0}".format(cid))
            #     #p = subprocess.run(["/usr/bin/docker", "checkpoint", str(cid),"ckclient"], stdout=subprocess.PIPE)
            #     print("FNC - Create a checkpoint with the command: \n\t docker checkpoint create {0} ckclient ".format(cid))
            #     time.sleep(3)
            #     print("FNC - Restore the checkpoint with the command: \n\t docker start --checkpoint ckclient sclient ")
            #     time.sleep(3)

        # else:
        #     conn.send(pickle.dumps({"action":"nothing"}))

    except KeyboardInterrupt:
        conn.close()
        print ("Connection closed")
        sys.exit()
print(received)
