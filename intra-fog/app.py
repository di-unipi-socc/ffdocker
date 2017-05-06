# Echo client program
import socket
import time
import pickle
import click
import subprocess
from multiprocessing import Pool
from multiprocessing import cpu_count

snode = "/tmp/ffsocket.sock"

# def f(x):
#     while True:
#         #time.sleep(2)
#         x*x
#
# def stress(num_cpu):
#     #processes = cpu_count()
#     pool = Pool(num_cpu)
#     print ('Utilizing {} cores\n'.format(num_cpu))
#     pool.map(f, range(num_cpu))


s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect(snode)

cid = socket.gethostname()
print("{0} - Application is running on container ....".format(cid))

# run the stress function
cpus = cpu_count() # numberof cpus of the host machine

p = subprocess.Popen(["/cpuburn", "-n", str(cpus)])
print("{0} - Burning {1} cores".format(cid, cpus))

time.sleep(5)
data = {"id": cid, "op": "increase"}
print("{0} - Sends :{1}".format(cid, data))
s.send(pickle.dumps(data))
resp = pickle.loads(s.recv(1024))
print('{0} - Received {1} '.format(cid, resp))
s.close()


time.sleep(10)
