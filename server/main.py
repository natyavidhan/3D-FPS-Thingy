import socket
from _thread import *
from threading import Thread
import sys
import random
import json
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = "localhost"
port = 5555
server_ip = socket.gethostbyname(server)
try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))
    
s.listen(10)
print("Waiting for a connection")

players = {}
mapSize = [100, 100]


def threaded_client(conn, addr):
    global players
    # players[str(addr)] = {"id": str(addr), "pos": [0, 10, 0], "rot": [0, 0, 0]}
    players[str(addr)] = [[0, 0, 0], [0, 0, 0], str(addr)]
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")
            if not data:
                conn.send(str.encode("Goodbye"))
                break
            message, command = reply.split("||")
            if message == "get":
                if command == "all":
                    conn.send(str.encode(json.dumps(players)))
                elif command == "self":
                    conn.send(str.encode(json.dumps(players[str(addr)])))
            elif message == "update":
                player = json.loads(command)
                player.append(str(addr))
                players[str(addr)] = player
                conn.send(str.encode("updated"))

        except Exception as e:
            traceback = sys.exc_info()[2].tb_lineno
            print(traceback)
            break
    print("Connection Closed")
    conn.close()
    players.pop(str(addr))


def server():
    while True:
        conn, addr = s.accept()
        print("Connected to: ", addr)
        start_new_thread(threaded_client, (conn, addr))

start_new_thread(server, ())
while True:
    pass