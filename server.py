import socket
from _thread import *
import pickle
from AQMController import AQMController

# server = "172.26.133.230"
server = "192.168.1.120"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
    s.bind((server,port))
except socket.error as e:  
    str(e)

s.listen()
print("Server Started, Waiting for a connection")

aqmc = AQMController()

connected = set()
clients = {}
idCount = 0

def threaded_AQM():
    global aqmc
    aqmc.controller()
    

def threaded_client(conn, clientId):
    global idCount
    global aqmc
    conn.send(str.encode(str(clientId)))
    reply = ""

    while True:
        try:
            data = conn.recv(4096).decode()

            if not data:
                break
            elif data == "get":
                reply = (aqmc.data_entries,
                        aqmc.minute_avg,
                        aqmc.hour_avg,
                        aqmc.day_avg)
                conn.sendall(pickle.dumps(reply))

        except:
            break

    print(len(pickle.dumps(aqmc)))

    print("Lost connection")
    
    try:
        del clients[clientID]
        print("Closing client", clientID)
    except:
        pass

    idCount -= 1
    conn.close()


start_new_thread(threaded_AQM,())

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    clientID = idCount

    start_new_thread(threaded_client, (conn, clientID))
