import socket
import threading

"""
STÁTUSZ KÓDOK:
0 - ENGEDÉLYADÁS AZ ÜZENETKÜLDÉSRE
1 - ÜZENETFOGADÁS / MEGJELENÍTÉS
2 - ÜZENETKÜLDÉS

EGYÉB JELZÉSEK:
/ - Elválasztó
"""

# Üzenetküldés függvény

def sendMessage(client):
    msg = input("Üzenet: ")
    client.send(f"2/{name}/{msg}".encode())

# Üzenetmegjelenítés függvény

def showMessage(data):
    usrname = data[1]
    message = data[2]
    print(f"{usrname}: {message}")

# Név megadása

name = input("\nKérem adjon meg egy felhasználónevet: ")
print("\n Kapcsolódás a szerverhez...\n")

# Kliens socket létrehozása, csatlakozás a szerverhez

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect(("127.0.0.1", 9999))
    client.send(name.encode())
except:
    print("Nem sikerült kapcsolódni a szerverhez.\n")

print("Sikeres csatlakozás a Chat-hez.\n")
print("Várakozás a többi felhasználó csatlakozására...\n")

# Kliensoldali chat logika

while True:
    received_data = client.recv(1024).decode()
    received_data = received_data.split("/")

    if received_data[0] == "0":
        if received_data[1] == name:
            sendMessage(client)
    elif received_data[0] == "1":
        showMessage(received_data)