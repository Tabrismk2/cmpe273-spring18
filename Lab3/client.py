import zmq
import sys
import threading

class Client:

    def __init__(self, username, addr_server, port_server):
        self.username = username
        context = zmq.Context() #ZMQ context
        self.sockREQ = context.socket(zmq.REQ)
        self.sockREQ.connect("tcp://%s:%s" % (addr_server, port_server))
        self.sockSUB = context.socket(zmq.SUB)
        self.sockSUB.setsockopt(zmq.SUBSCRIBE, b"")
        self.sockSUB.connect("tcp://%s:%s" % (addr_server, port_server+1))
        print("User[%s] Connected to the chat server." % (self.username))
    def msgReceiver(self):
        while True:
            username, message = self.sockSUB.recv_pyobj()
            if username != self.username:
                print("\r[%s]: %s\n[%s]>" % (username, message, self.username), end='')
            
            
    def msgSender(self):
        while True: 
            message = input("[%s]> " % (self.username))
            self.sockREQ.send_pyobj((self.username, message))
            ret = self.sockREQ.recv_string()
            if ret != "OK":
                print(ret)
           

    def start_client(self):
        thread_receive = threading.Thread(target = self.msgReceiver)
        thread_receive.start()
        self.msgSender()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python client.py [username]")
        raise SystemExit
    
    client = Client(sys.argv[1], "127.0.0.1", 5678)
    client.start_client()