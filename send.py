import socket

s = socket.socket()
on_server = 0
all_servers = ["Europe #1", "US #1", "Asia #1"]


def server_init():
    switch = {
        "Europe #1": "IP Here",
        "US #1": "IP Here",
        "Asia #1": "IP Here",
    }
    switch_port = {
        "Europe #1": "port here",
        "US #1": "port here",
        "Asia #1": "port here",
    }
    s.connect((switch.get(all_servers[on_server]), switch_port.get(all_servers[on_server])))


def send_to_machine(msg):
    s.send(str(msg).encode())


def receive_from():
    return str(s.recv(64000).decode())
