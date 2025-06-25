def user_agent(request, connection, response_not_found):
    headers = request.split(b"\r\n")[1:-2]  
    for header in headers:
        if header.startswith(b"User-Agent: "):
            user_agent = header.split(b": ", 1)[1]
            response = b"HTTP/1.1 200 OK\r\n" + b"Content-Type: text/plain\r\n" + b"Content-Length: " + str(len(user_agent)).encode() + b"\r\n\r\n" + user_agent
            connection.sendall(response)
            break
    connection.sendall(response_not_found)