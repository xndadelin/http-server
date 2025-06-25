import os

def make_file(request, connection, response_not_found, path, directory):
    try:
        headers, body = request.split(b"\r\n\r\n", 1)
        filename = path.split(b"/files/")[-1].decode()
        filepath = os.path.join(directory, filename)

        with open(filepath, "wb") as f:
            f.write(body)

        response = b"HTTP/1.1 201 Created\r\n\r\n"
        connection.sendall(response)
    except Exception as e:
        print(f"Error creating file: {e}")
        connection.sendall(response_not_found)