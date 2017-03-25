# Echo server program
#import socket,os
import os
import docker
from socket import *

client = docker.DockerClient(base_url='unix://var/run/docker.sock')

print(client.images.list())

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
    print(data)
    if not data: break
    conn.send(data)
conn.close()
