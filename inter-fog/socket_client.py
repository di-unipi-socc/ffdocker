# Echo client program
import socket
import time
import sys
import pickle

HOST = 'sserver'   # Symbolic name, meaning all available interfaces
PORT = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

cid = socket.gethostname()

s.connect((HOST, PORT))
print("App - Connected to {0}:{1}".format(HOST,PORT))
#time.sleep(2)
state = 0
while state < 100:
    try:
        d = {"id": cid, "state":state}
        s.send(pickle.dumps(d))
        time.sleep(1)
        print("App - sent     {0} ".format(d))
        resp = pickle.loads(s.recv(1024))
        print("App - received {0}".format(resp))
        if resp['action'] == "migrate":
            print("App - Perform action for migrating...")
            time.sleep(2)
            d = {"id": cid, "migrate":"yes"}
            s.send(pickle.dumps(d))
            print("App - sent    {0}".format(d))
            time.sleep(10)
        state += 1
    except socket.error:
        s.close()
        print("App - Socket closed")
        sys.exit()
    except KeyboardInterrupt:
        s.close()
        print ("App - Socket closed")
        sys.exit()

s.close()
