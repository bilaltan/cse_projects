# CSE 4057 Programming Assignment
# Bilal Tan - 150119630
# Sinem Onal - 150119576
# Abdülhalik Şensin - 150119598

import re
import socket
from threading import Thread
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme

server_public_key = RSA.import_key(open("server_public_key.pem",'rb').read())

def genRSAKeys():
    # Generate RSA Keys
	private_key = RSA.generate(2048)
	public_key = private_key.publickey().export_key()
	open("log.txt",'a').write("CLIENT: Key pair generated.\n")
	return private_key, public_key

def uploadImage(image_name):
	# Reading image
	image = open(image_name,'rb').read()

	# AES Encryption
	key = b'ABCDEF1234567890'
	iv = get_random_bytes(16)
	cipher = AES.new(key, AES.MODE_CBC, iv)
	enc_image = cipher.encrypt(pad(image, 16))

	# Signing Image
	signer = PKCS115_SigScheme(private_key)
	hash = SHA256.new(image)
	signature = signer.sign(hash)

	# Sending POST data to server
	sock.send(f"POST_IMAGE {image_name}".encode())
	data = b'IMG' + enc_image + b'SIG' + signature + b'KEY' + key + b'IV' + iv
	sock.send(data)

def downloadImage(image_name):
	sock.send(f"DOWNLOAD {image_name}".encode())

	# Receiving image data from server
	data = sock.recv(100000000)
	data_list = re.split(b'IMG|SIG|KEY|IV', data)
	
	# Splitting data to respective variable
	enc_image = data_list[1]
	signature = data_list[2]
	key = data_list[3]
	iv = data_list[4]

	# Decrypting image
	cipher = AES.new(key, AES.MODE_CBC, iv)
	image = unpad(cipher.decrypt(enc_image), 16)
	open(f"decrypted_{image_name}",'wb').write(image)
	open("log.txt",'a').write("CLIENT: Image downloaded.\n")

def getCertificate():
    # Certificate
	certificate = sock.recv(512)
	verifier = PKCS115_SigScheme(server_public_key)
	hash = SHA256.new(bytes(username+str(public_key),'utf-8'))

	try:
        # Verifier
		verifier.verify(hash, certificate)
		open("log.txt",'a').write("CLIENT: Certificate verified.\n")
	except:
		print("Invalid certificate. Closing connection...")
		return

def receive():
    while True:
        data = sock.recv(1024).decode("utf8")
        print(data)
	

host = 'localhost'
port = 20202
server = (host,port)
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect(server)

username = input("Enter username: ")
private_key, public_key = genRSAKeys()
sock.send(bytes(username,'utf-8'))
sock.send(public_key)

getCertificate()
Thread(target=receive).start()



choice = input("\nPOST(1) / DOWNLOAD(2) / EXIT(3): ")
while choice != '3':
	if choice == '1':	
		image_name = input("Enter image name to post: ")
		uploadImage(image_name)
	elif choice =='2':
		image_name = input("Enter image name to download: ")
		downloadImage(image_name)
	choice = input("\nPOST(1) / DOWNLOAD(2) / EXIT(3): ")
