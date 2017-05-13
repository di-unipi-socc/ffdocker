# Echo client program
import socket
import time
import sys
import pickle

# migrate containers by the FNC

HOST = 'selection'   # Symbolic name, meaning all available interfaces
PORT = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_fnc= socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)  # socket to fnc connection

#s_fnc.connect(snode)

cid = socket.gethostname()

s.connect((HOST, PORT))
print("Filtering - Connected to {0}:{1}".format(HOST,PORT))
#time.sleep(2)
state = 0
while state < 200:
    try:
        d = {"id": cid, "state":state}
        s.send(pickle.dumps(d))
        time.sleep(2)
        print("Filtering - sent {0} ".format(d))
        #resp = pickle.loads(s.recv(1024))
        #print("Filtering - received {0}".format(resp))
        # if resp['action'] == "migrate":
        #     print("App - Perform action for migrating...")
        #     time.sleep(2)
        #     d = {"id": cid, "migrate":"yes"}
        #     s.send(pickle.dumps(d))
        #     print("App - sent    {0}".format(d))
        #     time.sleep(10)
        state += 1
    except socket.error:
        s.close()
        print("Filtering - Socket closed")
        sys.exit()
    except KeyboardInterrupt:
        s.close()
        print ("Filtering - Socket closed")
        sys.exit()

s.close()
