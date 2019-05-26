import socket
from _thread import *
import pickle
port = 5555


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind(("localhost", port))
except socket.error as e:
    print(str(e))
s.listen(10)
print("Esperando Conexion")

players = [[696, 452, 0, 100], [550, 452, 0, 100]]


def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]
            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Conexion Perdida")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1

