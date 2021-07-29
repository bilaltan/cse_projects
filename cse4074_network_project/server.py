# CSE4074 Computer Network Programming Assignment
# Bilal Tan 150119630
# Selahattin Hüsmen 150119652

# Tested on 2 different computer in local network

import socket
import threading


class Server:
    def __init__(self):
        self.port = "port"

    def handleCLNT(self, clnt_connection): # Taking browser requests here
        try:
            request = clnt_connection.recv(1024).decode() # Request From Proxy Decoded Here

            requestParse = [] # Take browser entry
            a = request.split(" ") # We parse to browser entry- alternative for HTTPRequest library

            requestParse.append(a)


            try:
                url = int(requestParse[0][1][25:])# Take number on request for url
                print("GET", url)
            except ValueError: # If Client asks other than /Integer, server sends Bad request.
                url = requestParse[0][1][1:]

                data = "HTTP/1.1 400 Bad Request\r\n"
                data += "Content-Type: text/html; charset=utf-8\r\n"
                data += "\r\n"
                clnt_connection.sendall(data.encode()) # Sends Html response to the proxy server.
                pass

            url2 = requestParse[0][0]
            print(url2)

            try: # Take byte size 100-20000 otherwise not accept
                if url == "favicon.ico": # Pass favicon.ico
                    pass
                elif url2 != "GET": # Other than GET Requests result with Not Implemented.
                    data = "HTTP/1.1 501 Not Implemented\r\n"
                    data += "Content-Type: text/html; charset=utf-8\r\n"
                    data += "\r\n"
                    clnt_connection.sendall(data.encode()) # Sends Html response to the proxy server.
                elif 1000 > url >= 100:
                    data = "HTTP/1.1 200 OK\r\n"
                    data += "Content-Type: text/html; charset=utf-8\r\n"
                    data += "\r\n"
                    data += f"<html><head><title>I am {url} bytes long</title></head><body>\r\n\r\n"

                    for i in range(url - 88):
                        str = "a"
                        data = data + str
                    data = data + "</body></html>"
                    clnt_connection.sendall(data.encode()) # Sends Html response to the proxy server.
                elif 20000 >= url >= 1000:
                    data = "HTTP/1.1 200 OK\r\n"
                    data += "Content-Type: text/html; charset=utf-8\r\n"
                    data += "\r\n"
                    data += f"<html><head><title>I am {url} bytes long</title></head><body>\r\n\r\n"

                    for i in range(url - 89):
                        str = "a"
                        data = data + str
                    data = data + "</body></html>"
                    clnt_connection.sendall(data.encode())# Sends Html response to the proxy server.
                else:
                    data = "HTTP/1.1 400 Bad Request\r\n"
                    data += "Content-Type: text/html; charset=utf-8\r\n"
                    data += "\r\n"
                    clnt_connection.sendall(data.encode()) # Sends Html response to the proxy server.
            except ValueError:
                print("The input was not a valid integer.")

        except KeyboardInterrupt:
            print("\nShutting down...\n")
        except IOError as err:
            print("I/O error: {0}".format(err))
        except Exception as exc:
            print("Error:\n")
            print(exc)
        clnt_connection.close()

    def run(self, host, port): # Waiting for request form proxy
        server_sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sckt.bind((host, port))
        server_sckt.listen()
        print('Listening on port %s ...' % port)

        while True:
            clnt_connection, clnt_address = server_sckt.accept() # Create a new client connection.
            print("New Connection From {}".format(clnt_address))
            t = threading.Thread(target=self.handleCLNT, args=(clnt_connection,)) # Threading part.
            t.start()


if __name__ == "__main__": # Master server
    server = Server()
    server.run("192.168.0.23", 8080)
