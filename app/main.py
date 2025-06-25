import socket  # noqa: F401
from app.echo.main import echo
from app.user_agent.main import user_agent

def main():
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

    # respons with body /echo/{str} which must return a 200 OK response
    # Content-Type and Content-Length are required 

    if method == b"GET" and path == b"/":
        response = response_ok 
        connection.sendall(response) 
    elif method == b"GET" and path.startswith(b"/echo/"):
        echo(method, response_not_found, connection, path)
    elif method == b"GET" and path == b"/user-agent":
        user_agent(request, connection, response_not_found)
    else:
        connection.sendall(response_not_found)
        


if __name__ == "__main__":
    main()
