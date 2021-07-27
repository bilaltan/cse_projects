# CSE 4057 Programming Assignment
# Bilal Tan - 150119630
# Sinem Onal - 150119576
# Abdülhalik Şensin - 150119598

import os
import socket
from threading import Thread
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme

addr_client = {}
clients  = {}
private_key = RSA.generate(2048)
public_key = private_key.publickey().export_key()
open("server_public_key.pem",'wb').write(public_key)

def incoming_connection():
	while True:
		conn, client_addr = socket.accept()
		print(f"{client_addr} connected.")
		addr_client[conn] = client_addr
		Thread(target=client_connection, args=(conn,)).start()

def client_connection(conn):
	username = conn.recv(256).decode("utf8")
	clients[conn] = username
	client_public_key = conn.recv(512)

	# Creating and sending certificate
	signer = PKCS115_SigScheme(private_key)
	hash = SHA256.new(bytes(username+str(client_public_key),'utf-8'))
	certificate = signer.sign(hash)
	conn.send(certificate)
	open(f"{username}_cert.crt",'wb').write(certificate)
	open("log.txt",'a').write("SERVER: Certificate copy sent to client.\n")
	
	# Receiving POST or DOWNLOAD command
	command = conn.recv(32).decode()
	command = command.split(' ')
	function = command[0]
	image_name = command[1]

	if function == "POST_IMAGE":
		postImage(conn, username, image_name)
	elif function == "DOWNLOAD":
		downloadImage(conn, image_name)
	
def postImage(conn, username, image_name):
	# Receive image data
	data = conn.recv(100000000)

	# Saving image data in database
	os.makedirs(f"ServerData/{image_name}")
	open(f"ServerData/{image_name}/data.txt",'wb').write(data)
	
	# Sending new image message to all clients
	broadcastMessage(f"\nNEW_IMAGE {image_name} {username}")

def downloadImage(conn, image_name):
	# Reading image data from file
	data = open(f"ServerData/{image_name}/data.txt",'rb').read()
	conn.send(data)
	open("log.txt",'a').write("SERVER: Image data sent to client.\n")

def broadcastMessage(msg):
	# Sending message to all clients
	for sock in clients:
		sock.send(bytes(msg,"utf8"))


host = 'localhost'
port = 20202
addr = (host, port)
socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket.bind(addr)
socket.listen(5)

print("Waiting for connection...")
Thread(target=incoming_connection).start()
