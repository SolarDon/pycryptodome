from sys import exit, argv
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP

node = 1
message = "Encrypted data from EncryptData.py"

if __name__ == "__main__":
    for my_args in argv[1:]:
        variable,value = my_args.split('=')
        if variable == "node" :
            node =int(value)
            if node > 7 or node < 0:
                print "node needs to be between 0 and 7"
                exit(1)
                
file_in = open("encrypted_data.bin", "rb")
private_file = open("keys\N" + str(node) + "_private_key", 'rb')
#recipient_key = RSA.import_key(open("keys\N" + str(node) + "_public_key").read()
private_key = RSA.importKey(private_file.read(), "Node"+str(node))
enc_session_key, nonce, tag, ciphertext = \
   [ file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1) ]
# Decrypt the session key with the public RSA key
cipher_rsa = PKCS1_OAEP.new(private_key)
session_key = cipher_rsa.decrypt(enc_session_key)

# Decrypt the data with the AES session key
cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
data = cipher_aes.decrypt_and_verify(ciphertext, tag)
print data
