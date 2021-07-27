from Crypto.Cipher import AES
import hashlib,os

full_path = os.path.realpath(__file__)
password = b'pwmarmara'
key = hashlib.sha256(password).digest()
mode = AES.MODE_CBC
IV = 'marmara  marmara'

def pad_file(file):
    while len(file) % 16 != 0:
        file = file + b'0'
    return file

cipher = AES.new(key, mode, IV)

with open(os.path.dirname(full_path)+'/dog.jpg','rb') as f:
    original_file = f.read()

padded_file = pad_file(original_file)

encrypted_file = cipher.encrypt(padded_file)

with open('encrypted_file.txt', 'wb')as enc:
    enc.write(encrypted_file)

