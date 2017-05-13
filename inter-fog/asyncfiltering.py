# Echo client program
import socket
import time
import sys
import pickle
import asyncore  # handling asynch socket operation
import logging

# Filtering is the source component that generates the stream of integers.

HOST = 'selection'   # Symbolic name, meaning all available interfaces
PORT = 8888

logging.basicConfig(level=logging.DEBUG, format="%(created)-15s %(msecs)d %(levelname)8s  %(message)s")
log                     = logging.getLogger(__name__)

# "channel" communincatio to the fnc
class ChFnc(asyncore.dispatcher):

    def __init__(self, container_name, port):
        asyncore.dispatcher.__init__(self)
        self.write_buffer = {"op":23} #'GET %s HTTP/1.0\r\n\r\n' % self.url
        self.read_buffer = bytes(0)#= StringIO()
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        address = (container_name, port)
        log.info('connecting to %s', address)
        self.connect(address)

    def handle_connect(self):
        log.debug('handle_connect()')

    def handle_close(self):
        log.debug('handle_close()')
        self.close()

    def writable(self):
        #should return True, if you want the fd to be observed for write events;
        # is_writable = (len(self.write_buffer) > 0)
        # if is_writable:
        #      log.debug('writable() -> %s', is_writable)
        # return is_writable
        return False

    def readable(self):
        log.debug('readable() -> True')
        return True

    def handle_write(self):
        sent = self.send(pickle.dumps(self.write_buffer))
        log.debug('handle_write() -> ' )
        self.write_buffer = ""#sent#self.write_buffer[sent:]

    def handle_read(self):
        # is the socket is readable(),
        # call the dispatcher.recv() method for receiving to get the data
        #data = self.recv(8192)
        data = pickle.loads(self.recv(8192))
        log.debug('handle_read() -> {0}'.format(data))
        #self.read_buffer.write(data)

class ChSelection(asyncore.dispatcher):

    def __init__(self, container_name, port):
        asyncore.dispatcher.__init__(self)
        self.write_buffer = 0 #{"op":23} #'GET %s HTTP/1.0\r\n\r\n' % self.url
        #self.read_buffer = bytes(0)#= StringIO()
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        address = (container_name, port)
        log.info('connecting to %s', address)
        self.connect(address)

    def handle_connect(self):
        log.debug('handle_connect()')

    def handle_close(self):
        log.debug('handle_close()')
        self.close()

    def writable(self):
        #should return True, if you want the fd to be observed for write events;
        # is_writable = (len(self.write_buffer) > 0)
        # if is_writable:
        #      log.debug('writable() -> %s', is_writable)
        # return is_writable
        return True

    def readable(self):
        log.debug('readable() -> True')
        return False

    def handle_write(self):
        sent = self.send(pickle.dumps(self.write_buffer))
        log.debug('handle_write() -> ' )
        self.write_buffer += 1#sent#self.write_buffer[sent:]
        time.sleep(1)


    def handle_read(self):
        # is the socket is readable(),
        # call the dispatcher.recv() method for receiving to get the data
        #data = self.recv(8192)
        data = pickle.loads(self.recv(8192))
        log.debug('handle_read() -> {0}'.format(data))
        #self.read_buffer.write(data)

if __name__== "__main__":
    toFnc = ChFnc("127.0.0.1", 8083)
    toSelection = ChSelection("127.0.0.1",8888)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        print ("Filtering - Connection closed")
        asyncore.close_all()

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s_fnc= socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)  # socket to fnc connection
#
# #s_fnc.connect(snode)
#
# cid = socket.gethostname()
#
# s.connect((HOST, PORT))
# print("Filtering - Connected to {0}:{1}".format(HOST,PORT))
# #time.sleep(2)
# state = 0
# while state < 200:
#     try:
#         d = {"id": cid, "state":state}
#         s.send(pickle.dumps(d))
#         time.sleep(0.01)
#         print("Filtering - sent {0} ".format(d))
#         #resp = pickle.loads(s.recv(1024))
#         #print("Filtering - received {0}".format(resp))
#         # if resp['action'] == "migrate":
#         #     print("App - Perform action for migrating...")
#         #     time.sleep(2)
#         #     d = {"id": cid, "migrate":"yes"}
#         #     s.send(pickle.dumps(d))
#         #     print("App - sent    {0}".format(d))
#         #     time.sleep(10)
#         state += 1
#     except socket.error:
#         s.close()
#         print("Filtering - Socket closed")
#         sys.exit()
#     except KeyboardInterrupt:
#         s.close()
#         print ("Filtering - Socket closed")
#         sys.exit()
#
# s.close()