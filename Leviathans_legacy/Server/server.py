import socket
import threading
import sqlite3
import os


def connect_db():
    try:
        connection = sqlite3.connect("Leviathan.db")
        if os.path.isfile("Leviathan.db"):
            print("Connected to database")
            return connection
        else:
            raise ValueError('Failed to connect DB')
    except ValueError as e:
        print(f"Error with database connection: {e}")
        print("Shutting down")
        raise SystemExit


def handle_client(client_socket, addr):
    username = ""
    pid = 0
    try:
        connection = connect_db()
        querier = connection.cursor()
        while True:
            # receive and print client messages
            request = client_socket.recv(1024).decode("utf-8")
            if request.lower() == "close":
                break
            break_up = request.split(" ")
            if break_up[0] == "login":
                querier.execute("SELECT * FROM Players WHERE PName = ?", (break_up[1],))
                data = querier.fetchone()
                if data[0] == 0:
                    print('There is no profile named %s' % break_up[1])
                    response = "rejected"
                else:
                    print('Username %s found, pass is %s, given is %s' % (break_up[1], data[2], break_up[2]))
                    if break_up[2] == data[2]:
                        response = "accepted"
                        username = data[1]
                        pid = data[0]
                    else:
                        response = "rejected"
                client_socket.send(response.encode("utf-8")[:1024])
            elif break_up[0] == "info":
                querier.execute("SELECT * FROM Players WHERE PName = ?", (username,))
                data = querier.fetchone()
                response = ""
                for info in range(3, len(data)):
                    response += str(data[info])
                    if info != len(data):
                        response += " "
                print(response)
                client_socket.send(response.encode("utf-8")[:1024])
            elif break_up[0] == "info_buildings":
                querier.execute("SELECT * FROM Buildings WHERE PlayerID = ?", (pid,))
                data = querier.fetchall()
                response = ""
                for row in data:
                    response += str(row) + " "
                print(response)
                client_socket.send(response.encode("utf-8")[:1024])
            elif break_up[0] == "add_building":
                try:
                    querier.execute("INSERT INTO Buildings(PlayerID, BuildingNo, BuildingID, BuildingLevel) VALUES(?,?,?,?)", (pid, int(break_up[1]), int(break_up[2]), int(break_up[3]),))
                    connection.commit()
                except ValueError as e:
                    print(f"Error with building: {e}, could not assign building value {pid, break_up[1], break_up[2], break_up[3]}")
    except Exception as e:
        print(f"Error when handling client: {e}")
    finally:
        client_socket.close()
        print(f"Connection to client ({addr[0]}:{addr[1]}) closed")


def run_server():
    server_ip = "127.0.0.1"  # server hostname or IP address
    port = 8000  # server port number
    # Creation of server and connection
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to the host and port
        server.bind((server_ip, port))
        # listen for incoming connections
        print(f"Listening on {server_ip}:{port}")
        server.listen()
        while True:
            # accept a client connection
            client_socket, addr = server.accept()
            print(f"Accepted connection from {addr[0]}:{addr[1]}")
            # start a new thread to handle the client
            thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            thread.start()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.close()


run_server()
