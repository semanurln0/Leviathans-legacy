import socket
import threading
import sqlite3
import os


def handle_client(client_socket, addr):
    try:
        while True:
            # receive and print client messages
            request = client_socket.recv(1024).decode("utf-8")
            if request.lower() == "close":
                client_socket.send("closed".encode("utf-8"))
                break
            print(f"Received: {request}")
            # convert and send accept response to the client
            response = "accepted"
            client_socket.send(response.encode("utf-8"))
    except Exception as e:
        print(f"Error when hanlding client: {e}")
    finally:
        client_socket.close()
        print(f"Connection to client ({addr[0]}:{addr[1]}) closed")


def run_server():
    clients = []
    server_ip = "127.0.0.1"  # server hostname or IP address
    port = 8000  # server port number
    # Database connection error handling
    try:
        connection = sqlite3.connect("Leviathan.db")
        if os.path.isfile("Leviathan.db"):
            connection.cursor()
            print("Connected to database")
        else:
            raise ValueError('Failed to connect DB')
    except ValueError as e:
        print(f"Error with database connection: {e}")
        print("Shutting down")
        raise SystemExit
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
            thread = threading.Thread(target=handle_client, args=(client_socket, addr,))
            thread.start()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.close()


run_server()
