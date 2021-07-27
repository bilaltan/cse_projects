from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_PSS
import os,base64

print('')
print(' -- Part 1 -- ')

key = RSA.generate(2048) # Generating RSA Keys
f = open('public.pem', 'wb')
f.write(key.publickey().exportKey('PEM')) # Public Key Generation
f.close()
f = open('private.pem', 'wb')
f.write(key.exportKey('PEM')) # Private Key Generation
f.close()

file = open('public.pem', 'rb')
file2 = open('private.pem', 'rb')

public_key = RSA.importKey(file.read()) # Reading keys from files
private_key = RSA.importKey(file2.read())
print('Public Key:')
print(public_key.exportKey())
print('Private Key:')
print(private_key.exportKey())

print('')
print(' -- Part 2 -- ', '\n')

sym_key1 = os.urandom(16) # Symmetric Key generation 128 Bit
sym_key2 = os.urandom(32) # 256 Bit

print('')
print('AES-128 Key: ')
print(base64.b64encode(sym_key1))
print('')
encryption1 = public_key.encrypt(sym_key1,16) # Encryption with Public Key 
print('Encrypted 128 Bit Key with Public Key: ')
print(encryption1[0].hex())
print('')
decryption1 = private_key.decrypt(encryption1) # Decryption with Private Key 
print('Decrypted 128 Bit Key with Private Key: ')
print(base64.b64encode(decryption1),'\n')


print('AES-256 Key:')
print(base64.b64encode(sym_key2))
print('')
encryption2 = public_key.encrypt(sym_key2,32)
print('Encrypted 256 Bit Key with Public Key: ')
print(encryption2[0].hex())
print('')
decryption2 = private_key.decrypt(encryption2)
print('Decrypted 256 Bit Key with Public Key: ')
print(base64.b64encode(decryption2), '\n')


print(' -- Part 3 -- ', '\n')

long_string_m = 'meaningful text' * 75000 # 1.1 Megabytes Long String
print('Long String M: 75.000 times "meaningful text" which has 1.1mb size','\n')
hashed = SHA256.new()
hashed.update(long_string_m.encode('utf-8')) # Long String SHA256 Hashing 
print('SHA256 Hashed Long String M, H(M) --> ', hashed.hexdigest(), '\n') # Hashed String
signer = PKCS1_PSS.new(private_key) # Signer
signature = signer.sign(hashed) # Signed Text
print('Signature, Ka-(H(M)): ',signature.hex(), '\n')

print('First Signature Check with True Input: ')
try:
    hash_decrypt = PKCS1_PSS.new(public_key).verify(hashed,signature) # Public Key Decryption & Verification
    print(hash_decrypt, '<-- This returns if public key is verified') 
    print('Signature is Verified.')
    print('Ka+(Ka-(H(M))) -->', hashed.hexdigest(),'\n')
except Exception: # We sure that Hashed --> Encrypted --> Decrypted is verified.
    print('Not Valid.')


false_input = 'This is False Input'
print('Second Signature Check with False Input: ')
try:
    hash_decrypt = PKCS1_PSS.new(public_key).verify(false_input,signature) # Public Key Decryption & Verification
    print(hash_decrypt, '<-- This returns if public key is verified') 
    print('Signature is Verified.')
    print('Ka+(Ka-(H(M))) -->', hashed.hexdigest()) 
except Exception: # We sure that Hashed --> Encrypted --> Decrypted is verified.
    print(' -- ! Not Valid ! --')