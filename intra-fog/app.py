# Echo client program
import socket
import time
import pickle
import random
import click
import numpy
import subprocess
from multiprocessing import cpu_count

#snode = "/tmp/ffsocket.sock"

@click.command()
@click.option('--snode', default="/tmp/ffsocket.sock", help='Path of the socket file to communicate with the fog node controller')
@click.option('--tburn',default=2, help="Time for a single burn.")
def run(snode,tburn):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect(snode)

    range_cpus = 4  # max range of amount cpus tb be requested
    time_burn = tburn  # time duration of a single burn
    actual_cpus = 0    # numbetr of cpus actually used by the appliocation
    amount_cpus = 0   # number of cpu to increase/decrease

    init_time = time.clock()
    coord_chart = "(0,0)"  # coordinate per chart on latex
    response_times = []

    cid = socket.gethostname()
    print("App - is running on container {0}....".format(cid))

    # handshake with the FNC, asks the number of core to burn
    data = {"id": cid, "op": "setup", "actual":actual_cpus, "amount":amount_cpus}
    print("App - Send request {1}".format(cid, data))
    s.send(pickle.dumps(data))
    resp = pickle.loads(s.recv(1024))
    print('App - Receive response {1} '.format(cid, resp))
    actual_cpus = resp['cpus']
    coord_chart +="({0},{1})".format(time.clock()-init_time, actual_cpus)
    print(coord_chart)


    # try to burn all the cores (while the fnc has setted only a subset of cores)
    process = subprocess.Popen(["/cpuburn"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)#, "-n", str(cpus)])
    print("App - Burning {1} cores for {2} secs".format(cid, actual_cpus, time_burn))

    time.sleep(time_burn)

    for c in range(1,6):
        amount_cpu = random.randrange(1, 4) # max amount of  cores to be asked
        if random.uniform(0,1) > 0.5:
            data = {"id": cid, "op": "increase", "actual": actual_cpus, "amount":amount_cpu}
        else:
            data = {"id": cid, "op": "decrease", "actual": actual_cpus, "amount":amount_cpu}
        print("App - Send request {1}".format(cid, data))
        start_time = time.clock()
        s.send(pickle.dumps(data))
        resp = pickle.loads(s.recv(1024))
        stop_time = time.clock()
        response_time = stop_time - start_time
        response_times.append(response_time)
        print ("App - Response in {0} secs".format(response_time))
        #print('App - Receive response {1} '.format(cid, resp))
        print("App - Burning {1} cores for {2} secs".format(cid, resp['cpus'], time_burn))
        actual_cpus = resp['cpus']
        coord_chart +="({0},{1})".format(c*time_burn + response_time , actual_cpus)
        time.sleep(time_burn)
    s.close()
    process.kill()
    print(coord_chart)
    print(numpy.mean(response_times))
if __name__ == '__main__':
    run()
