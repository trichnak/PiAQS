import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(0.5)
        # self.server = "192.168.1.43"
        self.server = "192.168.1.120"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))

            data = b""
            while True:
                packet = self.client.recv(2048)
                if not packet: 
                    break
                data += packet

        except socket.error as e:
            print(e)
            return pickle.loads(data)
        
        