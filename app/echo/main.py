def echo(method, response_not_found, connection, path):
    string = path.split(b'/')[2]
    response = b"HTTP/1.1 200 OK\r\n" +  b"Content-Type: text/plain\r\n" + b"Content-Length: " + str(len(string)).encode() + b"\r\n\r\n" + string

    connection.sendall(response)