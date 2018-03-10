import zmq
import sys

class Server:
    def __init__(self, port1, port2):

        context = zmq.Context()
        
        self.sockREP = context.socket(zmq.REP)
        self.sockREP.bind("tcp://*:%s" %(str(port1)))
        self.sockPUB = context.socket(zmq.PUB)
        self.sockPUB.bind("tcp://*:%s" %(str(port2)))

    def run(self):
        while True:
            username, message = self.sockREP.recv_pyobj()
            self.sockREP.send_string("OK")
            self.sockPUB.send_pyobj((username, message))
    
if __name__ == "__main__":
    serve = Server(5678,5679)
    serve.run()    