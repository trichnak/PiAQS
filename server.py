# import socket
# from _thread import *
# import pickle
# from AQMController import AQMController

# server = "192.168.1.121"
# # server = "YOUR_SERVER_IP"
# port = 5555

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# try:
#     s.bind((server,port))
# except socket.error as e:  
#     str(e)

# s.listen()
# print("Server started, collecting data")

# aqmc = AQMController()

# connected = set()
# clients = {}
# idCount = 0

# def threaded_AQM():
#     global aqmc
#     aqmc.controller()
    

# def threaded_client(conn, clientId):
#     global idCount
#     global aqmc
#     conn.send(str.encode(str(clientId)))
#     reply = ""

#     while True:
#         try:
#             data = conn.recv(4096).decode()

#             if not data:
#                 break
#             elif data == "get":
#                 reply = (aqmc.data_entries,
#                         aqmc.minute_avg,
#                         aqmc.hour_avg,
#                         aqmc.day_avg)
#                 conn.sendall(pickle.dumps(reply))

#         except:
#             break

#     print("Lost connection")
    
#     try:
#         del clients[clientID]
#         print("Closing client", clientID)
#     except:
#         pass

#     idCount -= 1
#     conn.close()


# start_new_thread(threaded_AQM,())

# while True:
#     conn, addr = s.accept()
#     print("Connected to:", addr)

#     idCount += 1
#     clientID = idCount

#     start_new_thread(threaded_client, (conn, clientID))
# Import necessary modules and classes
import socket  # For creating sockets
from _thread import *  # For threading
import pickle  # For serializing and deserializing data
from AQMController import AQMController  # Custom class for controlling Air Quality Monitoring

# Set server IP address and port number
server = "192.168.1.121"  # Replace with your server's IP address
# server = "YOUR_SERVER_IP"
port = 5555  # Port number to use for communication

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Bind the socket to the specified IP address and port number
    s.bind((server,port))
except socket.error as e:  
    # If binding fails, print the error message
    str(e)

# Start listening for incoming connections
s.listen()
print("Server started, collecting data")

# Create an instance of the AQMController class
aqmc = AQMController()

# Initialize sets and dictionaries to keep track of connected clients
connected = set()  # Set to store connected client IDs
clients = {}  # Dictionary to store client connections
idCount = 0  # Counter to assign unique IDs to clients

# Define a function to run the AQM controller in a separate thread
def threaded_AQM():
    global aqmc  # Use the global AQMController instance
    aqmc.controller()  # Run the controller method

# Define a function to handle client connections in separate threads
def threaded_client(conn, clientId):
    global idCount  # Use the global ID counter
    global aqmc  # Use the global AQMController instance
    
    # Send the client ID to the client
    conn.send(str.encode(str(clientId)))
    
    reply = ""  # Initialize an empty reply string
    
    while True:
        try:
            # Receive data from the client (up to 4096 bytes)
            data = conn.recv(4096).decode()
            
            if not data:
                # If no data is received, break out of the loop
                break
            elif data == "get":
                # If the client sends "get", send back the current data entries and averages
                reply = (aqmc.data_entries,
                        aqmc.minute_avg,
                        aqmc.hour_avg,
                        aqmc.day_avg)
                conn.sendall(pickle.dumps(reply))  # Serialize and send the reply
                
        except:
            # If any exception occurs, break out of the loop
            break
    
    print("Lost connection")
    
    try:
        # Remove the client from the clients dictionary
        del clients[clientID]
        print("Closing client", clientID)
    except:
        pass
    
    # Decrement the ID counter
    idCount -= 1
    
    # Close the client connection
    conn.close()

# Start the AQM controller thread
start_new_thread(threaded_AQM,())

while True:
    # Accept incoming connections
    conn, addr = s.accept()
    print("Connected to:", addr)
    
    # Increment the ID counter and assign a new client ID
    idCount += 1
    clientID = idCount
    
    # Start a new thread to handle the client connection
    start_new_thread(threaded_client, (conn, clientID))