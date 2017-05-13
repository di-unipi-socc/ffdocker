import logging
import asyncore
import socket
import pickle
import time
#%(thread)d %(name)s

logging.basicConfig(level=logging.DEBUG, format="%(created)-15s %(msecs)d %(levelname)8s  %(message)s")
log                     = logging.getLogger(__name__)

BACKLOG                 = 5
SIZE                    = 1024

class EchoHandler(asyncore.dispatcher):

    def __init__(self, conn_sock, client_address, server):
        self.server             = server
        self.client_address     = client_address
        self.buffer             = {"id":"fnc", "op":"migrate"}

        # We dont have anything to write, to start with
        self.is_writable        = True

        # Create ourselves, but with an already provided socket
        asyncore.dispatcher.__init__(self, conn_sock)
        log.debug("created handler; waiting for loop")

    def readable(self):
        return False     # We are always happy to read

    def writable(self):
        return self.is_writable # But we might not have
                                # anything to send all the time

    def handle_read(self):
        log.debug("handle_read")
        data = pickle.loads(self.recv(SIZE))
        log.debug("after recv {0}".format(data))#.decode("utf-8")))
        if data:
            log.debug("got data")
            #self.buffer += data
            self.is_writable = True  # sth to send back now
        else:
            log.debug("got null data")

    def handle_write(self):
        log.debug("handle_write")
        if self.buffer:
            sent = self.send(pickle.dumps(self.buffer))
            log.debug("sent data")
            #self.buffer = {}
            #self.buffer = self.buffer[sent:]
        else:
            log.debug("nothing to send")
        if len(self.buffer) == 0:
            self.is_writable = False
        time.sleep(1)

    # Will this ever get called?  Does loop() call
    # handle_close() if we called close, to start with?
    def handle_close(self):
        log.debug("handle_close")
        log.info("conn_closed: client_address=%s:%s" % \
                     (self.client_address[0],
                      self.client_address[1]))
        self.close()
        #pass

class EchoServer(asyncore.dispatcher):

    allow_reuse_address         = False
    request_queue_size          = 5
    address_family              = socket.AF_INET
    socket_type                 = socket.SOCK_STREAM

    def __init__(self, address, handlerClass=EchoHandler):
        self.address            = address
        self.handlerClass       = handlerClass

        asyncore.dispatcher.__init__(self)
        self.create_socket(self.address_family,
                               self.socket_type)

        #if self.allow_reuse_address:
        self.set_reuse_addr()

        self.server_bind()
        self.server_activate()

    def server_bind(self):
        self.bind(self.address)
        log.debug("bind: address=%s:%s" % (self.address[0], self.address[1]))

    def server_activate(self):
        self.listen(self.request_queue_size)
        log.debug("listen: backlog=%d" % self.request_queue_size)

    def fileno(self):
        return self.socket.fileno()

    def serve_forever(self):
        try:
            asyncore.loop()
        except KeyboardInterrupt:
            print ("FNC - Connection closed")
            asyncore.close_all()


    # TODO: try to implement handle_request()
    # def handle_request(self):
    #     log.info("Handle request -> fnc")
    #
    # Internal use
    def handle_accept(self):
        (conn_sock, client_address) = self.accept()
        if self.verify_request(conn_sock, client_address):
            self.process_request(conn_sock, client_address)

    def verify_request(self, conn_sock, client_address):
        return True

    def process_request(self, conn_sock, client_address):
        log.info("conn_made: client_address=%s:%s" % \
                     (client_address[0],
                      client_address[1]))
        self.handlerClass(conn_sock, client_address, self)

    def handle_close(self):
        self.close()

if __name__ == "__main__":
     interface = "0.0.0.0"
     port = 8083
     server = EchoServer((interface, port))
     server.serve_forever()