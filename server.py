import socket
import threading

"""
STÁTUSZ KÓDOK:
1 - ÜZENETFOGADÁS / MEGJELENÍTÉS
2 - ÜZENETKÜLDÉS

EGYÉB JELZÉSEK:
/ - Elválasztó
"""
connected_clients = 0
users = {}

# Új kapcsolatok kezelése függvény

def handleNewConnection(server):
    while True:
        # A kapcsolatok fogadása, nyilvántartása

        client, addr = server.accept()

        usrname = client.recv(1024).decode()

        print(f"Új kliens csatlakozott: {usrname}, {client}")
        users[usrname] = client
        connected_clients += 1
        t_input_listener = threading.Thread(target=listenForMessage, args=(client,))
        t_input_listener.start()

# Küldő függvény (Replikáció)

def sender(forwardable_data, senderUser):
    for user in users:
        if user != senderUser:
            users[user].send(forwardable_data.encode())

# Új üzenet listener függvény

def listenForMessage(client):
    while True:
        data = client.recv(1024).decode()
        if data:
            data = data.split("/")
            senderUser = data[1]
            if data[0] == "2":
                data[0] = "1"
                forwardable_data = "/".join(data)
                sender(forwardable_data, senderUser)
            else:
                pass
                    
# Szerver socket létrehozása, bindelés, és listenelés kapcsolatokért

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("127.0.0.1", 9999))
server.listen()

t_connection_listener = threading.Thread(target=handleNewConnection, args=(server,))
t_connection_listener.start()