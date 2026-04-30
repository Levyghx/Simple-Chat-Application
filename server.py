import socket
import threading

"""
AZ ÜZENETEK FELÉPÍTÉSE:
TÍPUSKÓD / KÜLDŐ NEVE / TARTALOM

THE ARCHITECTURE OF MESSAGES:
TYPE / SENDER USERNAME / CONTENT

TÍPUSKÓDOK / TYPES:
000 - ÉRVÉNYTELEN FELHASZNÁLÓNÉV INVALID USERNAME
001 - ÉRVÉNYES FELHASZNÁLÓNÉV / VALID USERNAME
0 - KLIENS KEZDEMÉNYEZÉS / INITIAL CLIENT REQUEST
1 - ÜZENETFOGADÁS / RECEIVE MESSAGE
2 - ÜZENETKÜLDÉS / SEND MESSAGE

EGYÉB JELZÉSEK / OTHER SIGNALS:
/ - ELVÁLASZTÓ // SEPARATOR
"""
connected_clients = 0
users = {}

# Új kapcsolatok kezelése függvény / Handling new connections

def handleNewConnection():
    while True:
        # A kapcsolatok fogadása / Accepting connections

        client, addr = server.accept()

        t_input_listener = threading.Thread(target=listenForMessage, args=(client,))
        t_input_listener.start()

# Küldő függvény (Replikáció) / Replicator

def replicateMessage(forwardable_data, senderUser):
    for user in users:
        if user != senderUser:
            try:
                users[user].send(forwardable_data.encode())
            except:
                print(f"Nem sikerült elküldeni az üzenetet {user} felhasználónak.")

# Üzenetkezelő függvény / Message handler

def handleMessage(data, client):
    data = data.split("/")
    typeCode = data[0]
    username = data[1]
    content = data[2]

    if typeCode == "2":
        data[0] = "1"
        data = "/".join(data)
        replicateMessage(data, username)
    elif typeCode == "0":
        if username in users:
            client.send("000".encode())
        else:
            client.send("001".encode())
            users[username] = client
            print(f"Új user hozzáadva az adatlistához: {username}")

# Új üzenet listener függvény / Incoming message listener

def listenForMessage(client):
    while True:
        try:
            data = client.recv(1024).decode()
        except:
            for k in users:
                if users[k] == client:
                    users.pop(k)
                    break
            client.close()
            print("Egy kliens lecsatlakozott!")
            break
        else:
            handleMessage(data, client)
                    
# Szerver socket létrehozása, bindelés, és listenelés kapcsolatokért / Creating server socket, binding, listening for connections

global server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("127.0.0.1", 9999))
server.listen()

t_connection_listener = threading.Thread(target=handleNewConnection, args=())
t_connection_listener.start()