# Echo client program
import socket
import time
import pickle
import subprocess
from multiprocessing import Pool
from multiprocessing import cpu_count

snode = "/tmp/ffsocket.sock"

time_burn = 5
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect(snode)

cid = socket.gethostname()
print("App - is running on container {0}....".format(cid))

# handshake with the FNC, asks the number of core to burn
data = {"id": cid, "op": "setup", "actual":0}
print("App:{0} - Send request {1}".format(cid, data))
s.send(pickle.dumps(data))
resp = pickle.loads(s.recv(1024))
print('App:{0} - Receive response {1} '.format(cid, resp))
cpus = resp['cpus']


# try to burn all the cores (while the fnc has setted only a subset of cores)
process = subprocess.Popen(["/cpuburn"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)#, "-n", str(cpus)])
print("App:{0} - Burning {1}  cores for {2} secs".format(cid, cpus, time_burn))

time.sleep(time_burn)

# aks more cores
data = {"id": cid, "op": "increase", "actual": str(cpus)}
print("App:{0} - Send request {1}".format(cid, data))
s.send(pickle.dumps(data))
resp = pickle.loads(s.recv(1024))
print('App:{0} - Receive response {1} '.format(cid, resp))
print("App:{0} - Burning {1} cores for {2} secs".format(cid, resp['cpus'], time_burn))


time.sleep(time_burn)
s.close()
process.kill()
