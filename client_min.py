import socket
from threading import Thread

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 3001))


def listen(client):
    while True:
        data = client.recv(1024).decode("utf-8")
        if data:
            print(f"\rrecieved: {data}\nmsg: ", end="")
        else:
            continue


Thread(target=listen, args=(client,), daemon=True).start()

while True:
    msg = input("msg: ").encode("utf-8")
    if msg:
        client.send(msg)
