from sys import exit, argv
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

# first set defaults
message = 'To be signed and verified'
send_node = 1
recv_node = 2

if __name__ == "__main__":
    for my_args in argv[1:]:
        variable,value = my_args.split('=')
        if variable == "send" :
            send_node =int(value)
            if send_node > 7 or send_node < 0:
                print "send node needs to be between 0 and 7"
                exit(1)
        elif variable == "recv" :
            recv_node =int(value)
            if recv_node > 7 or recv_node < 0:
                print "recv node needs to be between 0 and 7"
                exit(1)                
        elif variable == "message":
            message = value
            
data = str.encode(message)
recipient_key = RSA.import_key(open("keys\N" + str(node) + "_public_key").read())
session_key = get_random_bytes(16)

# Encrypt the session key with the public RSA key
cipher_rsa = PKCS1_OAEP.new(recipient_key)
file_out = open("encrypted_data.bin", "wb")
file_out.write(cipher_rsa.encrypt(session_key))

# Encrypt the data with the AES session key
cipher_aes = AES.new(session_key, AES.MODE_EAX)
ciphertext, tag = cipher_aes.encrypt_and_digest(data)
[ file_out.write(x) for x in (cipher_aes.nonce, tag, ciphertext) ]
