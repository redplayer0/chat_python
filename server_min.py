import socket
import sys
from dataclasses import dataclass
from threading import Thread

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("localhost", 3001))
sock.listen(2)
print("listening...")

if len(sys.argv) > 1 and sys.argv[1] == "--relay":
    RELAY = True
else:
    RELAY = False


@dataclass
class Client:
    conn: str
    addr: str
    name: str = None


clients = []
state = []


def handle_client_relay(client):
    while True:
        data = client.conn.recv(1024).decode("utf-8")
        if data:
            # print(f"{client.name or client.addr} sent: {data}")
            relayed_msg = f"|{client.name or client.addr}:{data}"
            for c in clients:
                if c is not client:
                    c.conn.send(relayed_msg.encode("utf-8"))
        else:
            break

    print(f"\r{client.name or client.addr} disconnected\nserver message: ", end="")
    clients.remove(client)


def handle_client(client):
    while True:
        data = client.conn.recv(1024).decode("utf-8")
        if data:
            print(
                f"\r{client.name or client.addr} sent: {data}\nserver message: ",
                end="",
            )
            if "s" in data:
                state.append(data)
                print("\rstate:", state, "\nserver message: ", end="")
            if data.startswith("set_name "):
                client.name = data.split()[1]
        else:
            break

    print(f"\r{client.name or client.addr} disconnected\nserver message: ", end="")
    clients.remove(client)


def handle_new():
    while True:
        conn, addr = sock.accept()
        client = Client(conn, addr)
        print(f"\r{addr} connected\nserver message: ", end="")
        clients.append(client)
        if RELAY:
            Thread(target=handle_client_relay, args=[client]).start()
        else:
            Thread(target=handle_client, args=[client]).start()


if __name__ == "__main__":
    if RELAY:
        handle_new()
    else:
        Thread(target=handle_new, daemon=True).start()

        while True:
            msg = input("server message: ").encode("utf-8")
            if msg:
                for client in clients:
                    client.conn.send(msg)
