# Echo client program
import socket
import time
import pickle
import click
from multiprocessing import Pool
from multiprocessing import cpu_count

snode = "/tmp/ffsocket.sock"

def f(x):
    while True:
        time.sleep(1)
        x*x

def stress():
    processes = cpu_count()
    pool = Pool(processes)
    pool.map(f, range(processes))
    print ('Utilizing {} cores\n'.format(processes))

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect(snode)

cid = socket.gethostname()
print("Application is running on container: "+ cid)
data = {"id": cid, "op": "increase"}

print("Application sends :{0}".format( data))
s.send(pickle.dumps(data))
resp = pickle.loads(s.recv(1024))
print('Received:{0} '.format(resp))
s.close()

# run the stress function
stress()
