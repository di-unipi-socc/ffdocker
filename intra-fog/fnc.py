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
    print("FNC - Waiting for connection...")
    while True:
        try:
            #print("FNC - Accepted connection")
            data = pickle.loads(conn.recv(1024))
            print("FNC - Received: {0}".format(data))
            cid = data["id"] # container ID
            assigned_cpu = 0
            actual_cpus = data['actual']
            amount_cpus = data['amount']
            if data['op'] == "setup":
                assigned_cpu = n_cpus//2  # assign help of the Available CPUs
            elif data['op'] =="decrease":
                if actual_cpus - amount_cpus < 0:
                    assigned_cpu = 1
                    print("FNC - Error: {0} cpus are not available Cpus. Min cpus {1}".format(amount_cpus + actual_cpus, n_cpus))
                else:
                    assigned_cpu = actual_cpus - amount_cpus

            elif data['op'] =="increase":
                if(amount_cpus + actual_cpus > n_cpus):
                    assigned_cpu = n_cpus               # assigned all the CPUs
                    print("FNC - Error: {0} cpus are not available Cpus. Max cpus {1}".format(amount_cpus + actual_cpus, n_cpus))
                else:
                    assigned_cpu = amount_cpus + actual_cpus
            try:
                container = client.containers.get(cid)
                cpus = "0-"+str(assigned_cpu-1)

                thread = threading.Thread(target=async_update, args=(container,cpus))
                thread.start()

                for d in client.events(decode=True, filters={"container":cid}):
                    if d['Action'] =="update":
                        break

                print("FNC - Assigned {0} CPU  to container {1} ".format(assigned_cpu, cid))
                conn.send(pickle.dumps({"msg":"ok", "cpus":assigned_cpu}))
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
