# Echo client program
import socket
import time
import sys
import pickle

HOST = 'sserver'   # Symbolic name, meaning all available interfaces
PORT = 8888


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print("Connected to {0}{1}".format(HOST,PORT))
#time.sleep(2)
state = 0
while state < 20:
    try:
        d = {"state":state}
        s.send(pickle.dumps(d))
        time.sleep(1)
        print("sent{0} ".format(d))
        resp = pickle.loads(s.recv(1024))
        print("Client - received {0}".format(resp))
        if resp['action'] == "migrate":
            print("Client - Perform action for migrating...")
            s.send(pickle.dumps({"migrate":"yes"}))
            time.sleep(60)
        state += 1
    except socket.error:
        s.close()
        print("Socket closed")
        sys.exit()
    except KeyboardInterrupt:
        s.close()
        print ("Socket closed")
        sys.exit()
