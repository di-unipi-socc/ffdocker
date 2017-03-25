# Echo server program
#import socket,os
import os
import docker
from socket import *

client = docker.DockerClient(base_url='unix://var/run/docker.sock')
#container = client.contaiers.get("ff")
#container.update(cpuset_cpus="0,1")

#print(client.images.list())

s = socket(AF_UNIX, SOCK_STREAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
try:
    os.remove("/tmp/ffsocket")
except OSError:
    print(str(OSError))
    pass
s.bind("/tmp/ffsocket")
s.listen(1)
conn, addr = s.accept()
while 1:
    data = conn.recv(1024)
    if not data:
        break
    d = str(data)
    try:
        container = client.containers.get("ff")
        container.update(cpuset_cpus="0,1")
        print("updated to CPU:", "0,1")
    except docker.errors.NotFound as n:
        print (str(n))
    except docker.errors.APIError as a:
        print(str(a))
    conn.send(data)
conn.close()
