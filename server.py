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
        print(users)
        t_input_listener = threading.Thread(target=listenForMessage, args=(client, usrname,))
        t_input_listener.start()

# Küldő függvény (Replikáció)

def replicateMessage(forwardable_data, senderUser):
    for user in users:
        if user != senderUser:
            try:
                users[user].send(forwardable_data.encode())
            except:
                print(f"Nem sikerült elküldeni az üzenetet {user} felhasználónak.")

# Új üzenet listener függvény

def listenForMessage(client, usrname):
    while True:
        try:
            data = client.recv(1024).decode()
        except:
            client.close()
            try:
                users.pop(usrname)
            except:
                print(f"{usrname} nincs az adatlistában!")
            finally:
                print(f"{usrname} lecsatlakozott!")
                break
        else:
            data = data.split("/")
            senderUser = data[1]
            if data[0] == "2":
                data[0] = "1"
                forwardable_data = "/".join(data)
                replicateMessage(forwardable_data, senderUser)
            else:
                pass
                    
# Szerver socket létrehozása, bindelés, és listenelés kapcsolatokért

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("127.0.0.1", 9999))
server.listen()

t_connection_listener = threading.Thread(target=handleNewConnection, args=(server,))
t_connection_listener.start()