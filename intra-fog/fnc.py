# Echo server program
#import socket,os
import os
import docker
import click
import sys
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
        sys.exit()

    s.bind(snode)
    # for data in client.events(decode=True, filters={"Action":"update"}):
    #     print(data)
    print("FNC - Listen on socket: {0}".format(snode))
    s.listen(1)

    while True:
        print("FNC - Waiting for connection...")
        conn, addr = s.accept()
        try:
            print("FNC - Accepted connection")
            data = pickle.loads(conn.recv(1024))
            # if not data:
            #     break
            print("FNC - Received :{0}".format(data))
            try:
                cid = data["id"]
                container = client.containers.get(cid)
                container.update(cpuset_cpus="0,1")
                print("FNC - Assigned CPU {0} to container {1} ".format("0,1", cid))
                conn.send(pickle.dumps({"msg":"ok", "cpus":"0,1"}))
            except docker.errors.NotFound as n:
                print (str(n))
                pass
            except docker.errors.APIError as a:
                print(str(a))
                pass
        except KeyboardInterrupt:
            conn.close()
            print ("FNC - Connection closed")
            sys.exit()
        conn.close()

if __name__ == '__main__':
    run()
