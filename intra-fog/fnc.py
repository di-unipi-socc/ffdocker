# Echo server program
#import socket,os
import os
import docker
import click
import sys
import pickle
from socket import *
from multiprocessing import cpu_count
import threading

client = docker.DockerClient(base_url='unix://var/run/docker.sock')

def async_update(container, cpus):
    container.update(cpuset_cpus=cpus)

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

    n_cpus = cpu_count() # total number of CPUs on the host
    conn, addr = s.accept()
    while True:
        print("FNC - Waiting for connection...")

        try:
            print("FNC - Accepted connection")
            data = pickle.loads(conn.recv(1024))
            print("FNC - Received: {0}".format(data))
            cid = data["id"]
            assigned_cpu = 0
            if data['op'] == "setup":
                assigned_cpu = n_cpus -2  # assign 2 cpus (4-2)
            elif data['op'] =="increase":
                actual_cpus = data['actual']
                assigned_cpu = n_cpus  #- actual_cpus # assigned all the cpus
            try:
                container = client.containers.get(cid)
                cpus = "0-"+str(assigned_cpu-1)

                thread = threading.Thread(target=async_update, args=(container,cpus))
                #thread.daemon = True  # Daemonize thread
                thread.start()

                for d in client.events(decode=True, filters={"container":cid}):
                    if d['Action'] =="update":
                        break
                print("update done")
            # {'Action': 'update', 'status': 'update', 'time': 1494320263,
            # 'Actor': {'ID': '4caac1ef4d98895d4c6e32e93bb53a36769ab96b5a8e6f6094ddea2803c6a04f',
            # 'Attributes': {'image': 'diunipisocc/app', 'name': 'app'}}, 'timeNano': 1494320263468258516,
            # 'Type': 'container', 'id': '4caac1ef4d98895d4c6e32e93bb53a36769ab96b5a8e6f6094ddea2803c6a04f',
            # 'from': 'diunipisocc/app'}

                print("FNC - Assigned CPU {0} to container {1} ".format(cpus, cid))
                conn.send(pickle.dumps({"msg":"ok", "cpus":cpus}))
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
