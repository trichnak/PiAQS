# import socket
# import pickle

# class Network:
#     def __init__(self):
#         self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.client.settimeout(0.5)
#         self.server = "192.168.1.121"
#         # self.server = "YOUR_SERVER_IP"
#         self.port = 5555
#         self.addr = (self.server, self.port)
#         self.p = self.connect()

#     def getP(self):
#         return self.p

#     def connect(self):
#         try:
#             self.client.connect(self.addr)
#             return self.client.recv(2048).decode()
#         except:
#             pass

#     def send(self, data):
#         try:
#             self.client.send(str.encode(data))

#             data = b""
#             while True:
#                 packet = self.client.recv(2048)
#                 if not packet: 
#                     break
#                 data += packet

#         except socket.error as e:
#             return pickle.loads(data)
        
# Import necessary libraries
import socket  # Library for creating and using sockets
import pickle  # Library for serializing and deserializing data

# Define a class called Network
class Network:
    def __init__(self):
        # Create a new socket object
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
        # Set a timeout of 0.5 seconds on the socket
        self.client.settimeout(0.5)
        
        # Define the server IP address
        self.server = "192.168.1.121"
        
        # Define the port number to use for the connection
        self.port = 5555
        
        # Create a tuple containing the server IP address and port number
        self.addr = (self.server, self.port)
        
        # Call the connect method and store its return value in the 'p' attribute
        self.p = self.connect()

    # Define a method to get the value of 'p'
    def getP(self):
        return self.p

    # Define a method to establish a connection to the server
    def connect(self):
        try:
            # Attempt to connect to the server at the specified address and port
            self.client.connect(self.addr)
            
            # Receive data from the server (up to 2048 bytes) and decode it as a string
            return self.client.recv(2048).decode()
        except:
            # If an error occurs during connection, do nothing
            pass

    # Define a method to send data to the server and receive a response
    def send(self, data):
        try:
            # Encode the data as a string and send it to the server
            self.client.send(str.encode(data))
            
            # Initialize an empty byte string to store the received data
            data = b""
            
            # Enter a loop to receive data from the server in chunks
            while True:
                # Receive up to 2048 bytes of data from the server
                packet = self.client.recv(2048)
                
                # If no data is received, break out of the loop
                if not packet: 
                    break
                
                # Add the received data to the 'data' byte string
                data += packet
        
        except socket.error as e:
            # If a socket error occurs, deserialize the received data using pickle and return it
            print(e)
            return pickle.loads(data)