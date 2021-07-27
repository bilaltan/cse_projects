from Crypto.Cipher import AES
import hashlib

password = b'pwmarmara'
key = hashlib.sha256(password).digest()
mode = AES.MODE_CBC
IV = 'marmara  marmara'

cipher = AES.new(key,mode,IV)

with open('encrypted_file.txt','rb' ) as enc:
    encrypted_file = enc.read()

decrypted_file = cipher.decrypt(encrypted_file)

with open('decrypted_dog2.jpg', 'wb') as df:
    df.write(decrypted_file.rstrip(b'0'))