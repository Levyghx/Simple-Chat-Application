import socket
import random
import threading

"""
STÁTUSZ KÓDOK:
1 - ÜZENETFOGADÁS / MEGJELENÍTÉS
2 - ÜZENETKÜLDÉS

EGYÉB JELZÉSEK:
/ - Elválasztó
"""
connected_clients = 0
clients = []
listening_clients = []
users = []

# Szerver socket létrehozása

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Új kapcsolatok kezelése függvény

def handleNewConnection():
    while True:
        # A kapcsolatok fogadása, nyilvántartása

        client, addr = server.accept()

        usrname = client.recv(1024).decode()

        print(f"Új kliens csatlakozott: {usrname}, {client}")
        clients.append(client)
        users.append(usrname)
        t_input_listener = threading.Thread(target=listenForMessage, args=(client,))
        t_input_listener.start()

# Küldő függvény (Replikáció)

def sender(forwardable_data):
    for client in clients:
        client.send(forwardable_data.encode())

# Új üzenet listener függvény

def listenForMessage(client):
    while True:
        data = client.recv(1024).decode()
        if data:
            data = data.split("/")
            if data[0] == "2":
                data[0] = "1"
                forwardable_data = "/".join(data)
                sender(forwardable_data)
            else:
                pass
                    
# bindelés, és listenelés kapcsolatokért


server.bind(("127.0.0.1", 9999))

server.listen()

t_connection_listener = threading.Thread(target=handleNewConnection, args=())
t_connection_listener.start()