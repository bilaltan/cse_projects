from Crypto.Cipher import AES
import hashlib

pw = b'mypassword'
key = hashlib.sha256(pw).digest()
mode = AES.MODE_CBC
IVector = 'marmarauniversty'

def pad_file(file):
    while len(file) % 16 !=0:
        file = file + b'0'
    return file

cipher = AES.new(key,mode,IVector)

with open('/home/betan/Desktop/projects/sec/dog.jpg','rb') as file:
    original_file = file.read()

padded_file = pad_file(original_file)

encrypted_file = cipher.encrypt(padded_file)

print(encrypted_file.hex())

with open('encrypted_file', 'wb') as enc:
    enc.write(encrypted_file)

with open('/home/betan/Desktop/projects/encrypted_file', 'rb') as dec:
    enc_file = dec.read()

decrypted_file = cipher.decrypt(enc_file)

with open('decrypted_dog.txt', 'wb') as jpg:
    jpg.write(decrypted_file.rstrip(b'0'))
