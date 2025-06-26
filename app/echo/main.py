import gzip


def echo(method, response_not_found, connection, path, request):
    string = path.split(b'/')[2]
    headers = request.split(b"\r\n")[1:-2]
    accept_encoding = None
    for header in headers:
        if header.lower().startswith(b"accept-encoding:"):
            accept_encoding = header.split(b":", 1)[1].strip()
            break
    response = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n"
    body = string
    if accept_encoding:
        encodings = [e.strip() for e in accept_encoding.split(b",")]
        if b"gzip" in encodings:
            response += b"Content-Encoding: gzip\r\n"
            body = gzip.compress(string)
    response += b"Content-Length: " + str(len(body)).encode() + b"\r\n\r\n" + body
    connection.sendall(response)