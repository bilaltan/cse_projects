CSE 4057 Programming Assignment
Bilal Tan - 150119630
Sinem Onal - 150119576
Abdülhalik Şensin - 150119598

USAGE: First open server.py by typing python3 server.py to the command line.
After that connect the clients by typing python3 client.py to the command line.

You should type 1 for posting, 2 for downloading. After Typing 1 or 2, Enter the name of the file you want to download.

We used terminal for basic user interface.

In our project, we have implemented all the features required for the Image Sharing System specified in the project file.
First, We generate Public Key at the beginning.
Then Creating and sending certificate.
All the users have the public key of key server.

After that, one of the client should post image first. We will encrypt the image with AES in CBC mode. Iv generates randomly.
After encryption, client sign the encrypted file and send it to the server. Encripted file stored in ServerData.

Server receive the data and annouce all the clients that server has a new image. 

Other client can download the image by typing the name. This process will be the reverse of the post process. Server reads from file and send it to the client. Client decrypts the file.

If client certificate is not registered, connection will close.

We write all the messages to the log.txt.

For creation of multiple clients, we used threading library in python.
We used PyCryptodome library for AES / RSA / SHA256 and Signatures.
And also used socket for socket programming.
