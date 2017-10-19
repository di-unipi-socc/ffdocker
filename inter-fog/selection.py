# Echo client program
import socket
import time
from time import sleep
import os
import sys
import pickle
from threading import Timer
import threading

# from twisted.internet import task
# from twisted.internet import reactor


HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#s.setblocking(False)

class RepeatedTimer(object):
  def __init__(self, interval, function, *args, **kwargs):
    self._timer = None
    self.interval = interval
    self.function = function
    self.args = args
    self.kwargs = kwargs
    self.is_running = False
    self.next_call = time.time()
    #self.start()

  def _run(self):
    self.is_running = False
    self.start()
    self.function(*self.args, **self.kwargs)

  def start(self):
    if not self.is_running:
      self.next_call += self.interval
      self._timer = threading.Timer(self.next_call - time.time(), self._run)
      self._timer.start()
      self.is_running = True

  def stop(self):
    self._timer.cancel()
    self.is_running = False


#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
    print("Selection - bind on {0}:{1}".format(HOST,PORT))
except socket.error as msg:
    print ('Selection - Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()
s.listen(1)

print("Selection - Accepted connection ...")
conn, addr = s.accept()

s.setblocking(0)  # non blocking socket when it is connected

received = 0
prev_received = 0
sec = 0
stats = ""

def hello():
    global sec
    global prev_received
    global stats
    #if received > 100:
    stats += "({},{})".format(sec,received - prev_received)
    print(stats)
    if received == 1000:
        print ("Received {0} {1} ".format( received - prev_received, received))
    prev_received = received
    sec += 1

    #else:
    #    print ("Received {0}".format(received))

#print "starting..."

rt = RepeatedTimer(1, hello) # it auto-starts, no need of rt.start()

try:
    #sleep(5) # your long-running job goes here...
    data = pickle.loads(conn.recv(1024))

    rt.start()  # start the thradeing that count the received integer

    received += 1

    print("Selection - Received {0}".format(data))
    while True:
            try:
                data = pickle.loads(conn.recv(1024))
                #print("Selection - Received {0}".format(data))
                received += 1
                #print("Selection - Received {0}".format(data))

            except KeyboardInterrupt:
                conn.close()
                print ("Connection closed")
                sys.exit()
finally:
    rt.stop() # better in a try/finally block to make sure the program ends!
