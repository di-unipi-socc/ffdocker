# Echo client program
import socket
import time
from multiprocessing import Pool
from multiprocessing import cpu_count

def f(x):
    while True:
        x*x

def stress():
    processes = cpu_count()
    #print ('utilizing {} cores\n'.format(processes))
    pool = Pool(processes)
    pool.map(f, range(processes))
    print ('utilizing {} cores\n'.format(processes))

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect("/tmp/ffsocket")
s.send(b'Diminuisci cores')
data = s.recv(1024)
s.close()
print('Received ' + repr(data))

stress()

while True:
    time.sleep(20)
    print("jj")
