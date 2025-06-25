import socket  # noqa: F401


def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    response_ok = b"HTTP/1.1 200 OK\r\n\r\n"
    response_not_found = b"HTTP/1.1 404 Not Found\r\n\r\n"

    connection, address = server_socket.accept() # wait for client

    # extract url path
    # respond with either 200 or 404

    # a http request is made up of three parts, separated by CRLF (\r\n)
    # 1. request line
    # 2. zero or more headers
    # 3. an optional body

    request = connection.recv(1024)
    print(request.decode("utf-8"))
    
    request_line = request.split(b"\r\n")[0]
    method, path, _ = request_line.split(b" ")

    if method == b"GET" and path == b"/":
        connection.sendall(response_ok)
    else:
        connection.sendall(response_not_found)


if __name__ == "__main__":
    main()
