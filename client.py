import socket
import threading

"""
STÁTUSZ KÓDOK:
1 - ÜZENETFOGADÁS / MEGJELENÍTÉS
2 - ÜZENETKÜLDÉS

EGYÉB JELZÉSEK:
/ - Elválasztó
"""

# Üzenetmegjelenítés függvény

def showMessage(data):
    usrname = data[1]
    message = data[2]
    print(f"{usrname}: {message}")

# Új üzenet listener függvény

def listenForMessage(client):
    while True:
        received_data = client.recv(1024).decode()
        received_data = received_data.split("/")
        if received_data[0] == "1" and received_data[1] != name:
            showMessage(received_data)

# Input listener függvény

def listenForInput(client):
    while True:
        msg = input("")
        client.send(f"2/{name}/{msg}".encode())

# Kliens socket létrehozása

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Név megadása
name = input("\nKérem adjon meg egy felhasználónevet: ")
print("\n Kapcsolódás a szerverhez...\n")

# csatlakozás a szerverhez, szálak definiálása

try:
    client.connect(("127.0.0.1", 9999))
    client.send(name.encode())
except:
    print("Nem sikerült kapcsolódni a szerverhez.\n")
    quit()

t_message_listener = threading.Thread(target=listenForMessage, args=(client,))
t_input_listener = threading.Thread(target=listenForInput, args=(client,))

print("Sikeres csatlakozás a Chat-hez.\n")

t_message_listener.start()
t_input_listener.start()