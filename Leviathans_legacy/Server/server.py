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
    break_up = []
    try:
        while True:
            # receive and print client messages
            request = client_socket.recv(1024).decode("utf-8")
            connection = connect_db()
            querier = connection.cursor()
            print(request)
            if request.lower() == "close":
                break
            break_up = request.split(" ")
            print(break_up)
            if break_up[0] == "login":
                querier.execute("SELECT count(*) FROM Players WHERE PName = ?", (break_up[1],))
                data = querier.fetchone()
                # password = querier.fetchone()[1]
                if data[0] == 0:
                    print('There is no profile named %s' % break_up[1])
                    response = "rejected"
                    client_socket.send(response.encode("utf-8")[:1024])
                else:
                    print('Username %s found in %s row(s)' % (break_up[1], data))
                    # print(password)
                    response = "accepted"
                    client_socket.send(response.encode("utf-8")[:1024])
            print(f"Received: {request}")
            # convert and send accept response to the client
            response = "accepted"
            client_socket.send(response.encode("utf-8"))
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
