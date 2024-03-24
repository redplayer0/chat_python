from threading import Thread

from client import Client


def spawn_test_client():
    client = Client().connect()
    client.test()


Thread(target=spawn_test_client, daemon=True).start()

input("press enter to stop/exit..")
