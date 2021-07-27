import random
import time
from Crypto.Cipher import AES
from Crypto.Util import Counter

def encrypt(key, counter, data):
    aes = AES.new(key, AES.MODE_CTR,  counter=Counter.new(128, initial_value=counter))
    encrypted = aes.encrypt(data)
    return encrypted

def decrypt(key, counter, encrypted_text):
    aes = AES.new(key, AES.MODE_CTR,  counter=Counter.new(128, initial_value=counter))
    decrypted = aes.decrypt(encrypted_text)
    return decrypted

def write_encrypted_text(encrypted_message):
    with open("encrypted.txt", "w", encoding='latin-1') as f:
        f.write(encrypted_message)
        f.close()

def read_encrypted_text():
    with open("encrypted.txt", "r", encoding='latin-1') as f:
        m = f.read()
        decrypted_message = decrypt(key, counter, m.encode('latin-1'))
        return decrypted_message.decode('latin-1')

def write_decrypted_text(decrytped_text):
    with open("decrypted.txt", "w", encoding='latin-1') as f:
        f.write(decrytped_text)
        f.close()

key = b'\x00' * 32
counter = random.SystemRandom().randint(0,15)
data = b'meaningful text' * 75000 # 1.1 Megabytes Long String

encrypt_time = 0
decrypt_time = 0
start = time.time()
encrypted_message = encrypt(key, counter, data).decode('latin-1')
print(encrypted_message)
write_encrypted_text(encrypted_message) # enc ettik

encrypt_time = time.time() - start
start = time.time()

decrypted_message = read_encrypted_text() # dec ettik
write_decrypted_text(decrypted_message) # dec i yazdırdık

print(decrypted_message)
decrypt_time = time.time() - start
print("Encrypt time : "+str(encrypt_time))
print("Decrypt time : "+str(decrypt_time))

