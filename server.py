import socket
import threading
import time

list_of_connections = []
list_of_cords = []
all_indexes = []

s = socket.socket()
print("Socket Created...")
port = "port here"
s.bind(('', port))
print("Socket On:  %s" % (port))


def empty():
    on = len(list_of_connections) - 1
    while on not in all_indexes:
        on -= 1
    return on


def receiver(on):
    r = on

    print("Started Recv")
    run = True
    while run:
        try:
            try:
                list_of_cords[r] = list_of_connections[r][0].recv(1024).decode()
            except ConnectionResetError:
                print("Connection Lost: " + str(r))
                list_of_cords[r] = ""
                run = False
            except ConnectionAbortedError:
                print("Connection Lost: " + str(r))
                list_of_cords[r] = ""
                run = False
            except TimeoutError:
                print("Connection Lost: " + str(r))
                list_of_cords[r] = ""
                run = False
            except BrokenPipeError:
                print("Connection Lost: " + str(r))
                list_of_cords[r] = ""
                run = False

            try:
                list_of_connections[r][0].send(str(list_of_cords).encode())
            except ConnectionResetError:
                list_of_cords[r] = ""
                run = False
                print("Connection Lost: " + str(r))
            except ConnectionAbortedError:
                list_of_cords[r] = ""
                run = False
                print("Connection Lost: " + str(r))
            except TimeoutError:
                print("Connection Lost: " + str(r))
                list_of_cords[r] = ""
                run = False
            except BrokenPipeError:
                print("Connection Lost: " + str(r))
                list_of_cords[r] = ""
                run = False
        except IndexError:
            print("Skipped: " + str(r))


def connection_dealer():
    s.listen(5)
    print("Listening...")
    pending = s.accept()
    print("Got connection!")

    on__ = -1
    on_alt = 0
    breaker = False
    for x in list_of_cords:
        if x == "" and not breaker:
            print("Replaced Slot")
            on__ = on_alt
            breaker = True
            list_of_connections[on__] = pending
        on_alt += 1
    if on__ == -1:
        print("Accepted New")
        list_of_connections.append(pending)
        list_of_cords.append("")
        print("Current Connection Array Length: " + str(len(list_of_connections)))
        print("Current Cord Array Length: " + str(len(list_of_cords)))
        on__ = len(list_of_cords) - 1
    connector = threading.Thread(target=receiver, args=(on__,))
    connector.start()


if __name__ == '__main__':
    thread_new = threading.Thread(target=connection_dealer)
    while True:
        if not thread_new.is_alive():
            thread_new = threading.Thread(target=connection_dealer)
            thread_new.start()

# THIS IS THE BEST CURRENT VERSION
