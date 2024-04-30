import socket
from _thread import *
import pickle

server = "172.26.133.230"
# server = "192.168.1.43"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server,port))
except socket.error as e:  
    str(e)

s.listen()
print("Server Started, Waiting for a connection")

connected = set()
clients = {}
idCount = 0

def threaded_client(conn, p, clientId):
    global idCount
    conn.send(str.encode(str(p)))
    reply = ""

    while True:
        try:
            data = conn.recv(4096).decode()

            if clientID in clients:
                client = clients[clientID]

                if not data:
                    break
                else:
                    if data == "reset":
                        client.resetWent()
                    elif data != "get":
                        client.play(p, data)

                    reply = client
                    conn.sendall(pickle.dumps(reply))

            else:
                break
        except:
            break
    print("Lost connection")
    
    try:
        del clients[clientID]
        print("Closing client", clientID)
    except:
        pass

    idCount -= 1
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0
    clientID = (idCount - 1)//2
    if idCount % 2 == 1:
        clients[clientID] = Client(clientID)
        print("Creating a new client...\nID: ", clientID)
    else:
        clients[clientID].ready = True
        print("client ", clientID, " ready.")
        p = 1

    start_new_thread(threaded_client, (conn, p, clientID))
