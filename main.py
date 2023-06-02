from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
from person import Person

BUFSIZ = 1024

people = []
addresses = {}

HOST = ''
PORT = 55000

ADDR = (HOST, PORT)
MAX_CONNECTION = 10

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

client = person.client
name = person.name
addr = person.addr


def broadcast(msg, name):
    for person in people:
        client = person.client
        client.send(bytes(name + ": ", "utf8") + msg)


def client_communication(person):
    client = person.client
    addr = person.addr

    name = client.recv(BUFSIZ).decode("utf8")
    welcome = client.recv(
        f"Welcome to the reality with UnPerChat! If you ever want to quit it just type" + '{' + "quit" + '}!')
    msg = f"Unperson {name} has joined UnPerChat"
    broadcast(msg)

    run = True
    while run:
        try:
            msg = client.recv(BUFSIZ)
            if msg == bytes("{quit}", "utf8"):
                client.send(bytes(f"{quit}", "utf8"))
                people.remove(person)
                client.close()
            else:
                broadcast(msg, name)
        except Exception() as e:
            print("[EXCEPTION], e")
            run = False


def wait_for_connection(SERVER):
    run = True
    while run:

        try:
            client, addr = SERVER.accept()
            person = Person(addr, client)
            print(f"{client} has connected successfully at {time.time()}! {addr}")
            client.send(
                bytes("Hello, you enter the new reality - UnPerChat!Now type your name and press Enter1", "utf8"))
            people.append(person)

            Thread(target=client_communication, args=(person,)).start()
        except Exception as e:
            print("[FAILURE! TRY AGAIN!]", e)
            run = False

    print("SERVER CRASHED!")


if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTION)
    print("Please be patient, we are waiting for connection...")
    ACCEPT_THREAD = Thread(target=wait_for_connection, args=(SERVER,))
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()