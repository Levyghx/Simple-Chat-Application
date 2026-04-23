import socket
import random
import threading

"""
STÁTUSZ KÓDOK:
0 - ENGEDÉLYADÁS AZ ÜZENETKÜLDÉSRE
1 - ÜZENETFOGADÁS / MEGJELENÍTÉS
2 - ÜZENETKÜLDÉS

EGYÉB JELZÉSEK:
/ - Elválasztó
"""
connected_clients = 0
clients = []
users = []

# Szerver socket létrehozása, bindelés, és listenelés kapcsolatokért

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("127.0.0.1", 9999))

server.listen()

# A létrejött kapcsolatok kezelése, a chat szerveroldali logikája

while True:

    # A kapcsolatok fogadása, nyilvántartása

    client, addr = server.accept()

    usrname = client.recv(1024).decode()

    print(f"Új kliens csatlakozott: {usrname}, {client}")
    clients.append(client)
    users.append(usrname)
    connected_clients += 1

    # Szerveroldali chat logika




    """
    if connected_clients == 2:
        rnum = random.randint(0, len(users)-1)

        while True:
            chatting_usr = users[rnum]

            for client in clients:
                client.send(f"0/{chatting_usr}".encode())

            msg = clients[rnum].recv(1024).decode()
            msg = msg.split("/")

            for client in clients:
                client.send(f"1/{msg[0]}/{msg[1]}".encode())

            if rnum == 0:
                rnum = 1
            else:
                rnum = 0
    """