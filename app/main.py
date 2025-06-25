import socket  # noqa: F401


def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    response = b"HTTP/1.1 200 OK\r\nContent-Length: 13\r\n\r\nHello, World!"

    connection, address = server_socket.accept() # wait for client
    print(f"got connection from {address}")
    connection.sendall(response)  # send response


if __name__ == "__main__":
    main()
