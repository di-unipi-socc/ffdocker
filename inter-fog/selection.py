# Echo client program
import socket
import time
import os
import sys
import pickle

from twisted.internet import task
from twisted.internet import reactor


HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#s.setblocking(False)

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
while True:
        try:
            data = pickle.loads(conn.recv(1024))
            print("Selection - Received {0}".format(data))
            received += 1
        except KeyboardInterrupt:
            conn.close()
            print ("Connection closed")
            sys.exit()
#
# def receivedEverySecond():
#     global received
#     print("Second -> Received {0}".format(received))
#
# def receive_loop(conn):
#     global received
#     while True:
#         try:
#             data = pickle.loads(conn.recv(1024))
#             print("Selection - Received {0}".format(data))
#             received += 1
#         except KeyboardInterrupt:
#             conn.close()
#             print ("Connection closed")
#             sys.exit()
#             reactor.stop()
#
#
#
# l = task.LoopingCall(receivedEverySecond)
# l.start(1.0) # call every second
# reactor.callLater(0.01, receive_loop, conn)
# reactor.run()


# l.stop() will stop the looping calls
