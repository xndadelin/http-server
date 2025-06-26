import socket
import threading
import sys
from app.echo.main import echo
from app.user_agent.main import user_agent
from app.file.main import file
from app.make_file.main import make_file


def handle_client(connection, directory):
    response_ok = b"HTTP/1.1 200 OK\r\n\r\n"
    response_not_found = b"HTTP/1.1 404 Not Found\r\n\r\n"
    while True:
        try:
            request = b""
            while b"\r\n\r\n" not in request:
                chunk = connection.recv(1024)
                if not chunk:
                    return
                request += chunk

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

            headers = request.split(b"\r\n\r\n", 1)[0].split(b"\r\n")[1:]
            close = False
            for header in headers:
                if header.lower().startswith(b"connection:") and b"close" in header.lower():
                    close = True
                    break
            if close:
                break
        except Exception as e:
            print(f"Exception: {e}")
            break
    connection.close()


def main():
    directory = "/tmp"
    if "--directory" in sys.argv:
        idx = sys.argv.index("--directory")
        if idx + 1 < len(sys.argv):
            directory = sys.argv[idx + 1]
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        connection, address = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(connection, directory))
        thread.start()


if __name__ == "__main__":
    main()
