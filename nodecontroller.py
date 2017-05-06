# Echo server program
#import socket,os
import os
import docker
import click
import pickle
from socket import *

client = docker.DockerClient(base_url='unix://var/run/docker.sock')

@click.command()
@click.option('--snode', default="/tmp/ffsocket.sock", help='Path of the socket file to communicate with the node controller')
def run(snode):

    s = socket(AF_UNIX, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    try:
        if os.path.exists(snode):
            os.remove(snode)
    except OSError:
        print(str(OSError))
        pass
    s.bind(snode)
    for d in client.events(decode=True, filters={"Action":"update"}):
        print(d)

    while 1:
        print("Listen on socket: {0}".format(snode))
        s.listen(1)
        conn, addr = s.accept()
        print("Accepted connection :{0}".format(addr))
        d = pickle.loads(conn.recv(1024))
        #dict = (tcp_recieve())
        if not d:
            break
        #d = str(data)
        print("Received :{0}".format(d))
        try:
            container = client.containers.get(d["id"])
            container.update(cpuset_cpus="0,1")
            print("Updated to CPU:", "0,1")
        except docker.errors.NotFound as n:
            print (str(n))
            pass
        except docker.errors.APIError as a:
            print(str(a))
            pass


        conn.send(pickle.dumps({"msg":"ok"}))
    conn.close()

if __name__ == '__main__':
    run()
