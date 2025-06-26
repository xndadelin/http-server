def echo(method, response_not_found, connection, path, request):
    string = path.split(b'/')[2]
    
    headers = request.split(b"\r\n")[1:-2]
    accept_encoding = None
    for header in headers:
        if header.lower().startswith(b"accept-encoding:"):
            accept_encoding = header.split(b":", 1)[1].strip()
            break
    response = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n"
    if accept_encoding and b"gzip" in accept_encoding:
        response += b"Content-Encoding: gzip\r\n"
    response += b"Content-Length: " + str(len(string)).encode() + b"\r\n\r\n" + string
    connection.sendall(response)