# CSE4074 Computer Network Programming Assignment
# Bilal Tan 150119630
# Selahattin Hüsmen 150119652

# Tested on 2 different computer in local network

import socket

while True:

    try:
        # Client and Proxy connection
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sckt.bind(("192.168.0.19", 8888))
        # Listen to the client for a request
        sckt.listen()
        # Server and proxy connection
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect(("192.168.0.23", 8080))
        # Take clients address
        clnt_socket, address = sckt.accept()
        urlAskedFromClient = clnt_socket.recv(2048).decode()  # client to px
        # Parse to client address
        requestParse = []
        a = urlAskedFromClient.split(" ")
        requestParse.append(a)

        b = a[1].split("/")
        print(b[3])
        url = requestParse[0][1][1:]
        # Take data, byte size smaller then 9999. byte size is bigger then 9999 not accept
        if int(b[3])<9999:

            server.send(f"GET /{url}".encode())  # Sent to Server

            dataServerSent = server.recv(2094)  # Proxy received from server

            print(dataServerSent)

            clnt_socket.send(dataServerSent)  # Proxy to Client

        else:
            dataProxySent = "HTTP/1.1 414 Bad Request\r\nContent-Type: text/html; " \
                            "charset=utf-8\r\n\r\n<html><head><title>Error</title></head><body>414 " \
                            "Request-URI Too Long</body></html>"
            clnt_socket.sendall(dataProxySent.encode())

    except:
        pass
