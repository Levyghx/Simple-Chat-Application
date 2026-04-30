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
# Kezdeményezőfolyamat kezelő függvény / Initial connection handler

def handleInitialConnection():
    # csatlakozás a szerverhez, szál definiálása / connecting to the server, defining thread
    try:
        client.connect(("127.0.0.1", 9999))
        print("\nKapcsolódás a szerverhez...\n")
    except:
        print("Nem sikerült kapcsolódni a szerverhez.\n")
        quit()
    else:
        t_message_listener = threading.Thread(target=listenForMessage, args=())
        t_message_listener.start()
        starterFunction()

# Kezdő függvény / Starter function

def starterFunction():
    # Név megadása / Name input
    global name
    name = input("\nKérem adjon meg egy felhasználónevet: ")
    client.send(f"0/{name}/{name}".encode())

# Üzenetmegjelenítés függvény / Message displaying

def showMessage(data):
    usrname = data[1]
    message = data[2]
    print(f"{usrname}: {message}")

# Üzenetkezelő függvény / Message handler

def handleMessage(data):
    data = data.split("/")
    typeCode = data[0]

    if typeCode == "1":
        showMessage(data)
    elif typeCode == "000":
        print("\nÉrvénytelen név.")
        starterFunction()
    elif typeCode == "001":
        print("Sikeres csatlakozás a Chat-hez.\n")
        t_input_listener = threading.Thread(target=listenForInput, args=())
        t_input_listener.start()

# Új üzenet listener függvény / Incoming message listener

def listenForMessage():
    while True:
        try:
            received_data = client.recv(1024).decode()
        except:
            print("Megszakadt a kapcsolat.")
            break
        else:
            handleMessage(received_data)

# Input listener függvény / Input listener

def listenForInput():
    while True:
        msg = input("")
        try:
            client.send(f"2/{name}/{msg}".encode())
        except:
            print("Nem sikerült az üzenetet elküldeni.")
            break

# Kliens socket létrehozása / Creating client socket
global client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

handleInitialConnection()