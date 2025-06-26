import socket
import threading
import sys
from app.echo.main import echo
from app.user_agent.main import user_agent
from app.file.main import file
from app.make_file.main import make_file

# handle a single client connection

def handle_client(connection, directory):
    response_ok = b"HTTP/1.1 200 OK\r\n\r\n"
    response_not_found = b"HTTP/1.1 404 Not Found\r\n\r\n"
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
    elif method == b"GET" and path.startswith(b"/echo/"):
        echo(method, response_not_found, connection, path, request)
    elif method == b"GET" and path == b"/user-agent":
        user_agent(request, connection, response_not_found)
    elif method == b"GET" and path.startswith(b"/files"):
        file(request, connection, response_not_found, path, directory)
    elif method == b"POST" and path.startswith(b"/files"):
        make_file(request, connection, response_not_found, path, directory)
    else:
        connection.sendall(response_not_found)
    connection.close()


def main():
    directory = "/tmp"  # default
    if "--directory" in sys.argv:
        idx = sys.argv.index("--directory")
        if idx + 1 < len(sys.argv):
            directory = sys.argv[idx + 1]
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        connection, address = server_socket.accept() # wait for client
        thread = threading.Thread(target=handle_client, args=(connection, directory))
        thread.start()

if __name__ == "__main__":
    main()
