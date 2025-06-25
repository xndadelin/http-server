import os

def file(request, connection, response_not_found, path, directory):
    filename = path.split(b"/files/")[-1].decode()
    filepath = os.path.join(directory, filename)
    try:
        with open(filepath, "rb") as f:
            content = f.read()
        response = (
            b"HTTP/1.1 200 OK\r\n"
            b"Content-Type: application/octet-stream\r\n"
            b"Content-Length: " + str(len(content)).encode() + b"\r\n\r\n" + content
        )
        connection.sendall(response)
    except FileNotFoundError:
        connection.sendall(response_not_found)
