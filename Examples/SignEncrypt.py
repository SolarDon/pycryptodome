from sys import exit, argv
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

'''
This is to sign a document then encypt it.
This allows only the reciever can decrypt the data and that the data is from a verified source
'''

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
        else:
            print "Invalid input, valid inputs are\n\tsend=<send_node>\n\trecv=<recv_node\n\tmessage=<message>"
            exit(1)
            
# Read private key from file
secret_code = "Node" + str(send_node)
file_name = "keys\N"+str(send_node)+"_private_key"
private_key = RSA.import_key(open(file_name).read(), passphrase=secret_code )
digest = SHA256.new(message)
signature = pkcs1_15.new(private_key).sign(digest)

print len(signature), signature

# The signature now becomes part of the package along with a hint
data = signature + str(send_node)+ message
data = signature + "0" + message
print data
#data = 'To be signed and encrypted SignEncrypt.py'


recv_public_key_file = "keys\N"+str(recv_node)+"_public_key"
recipient_key = RSA.importKey(open(recv_public_key_file).read())
session_key = get_random_bytes(16)
# Encrypt the session key with the public RSA key
cipher_rsa = PKCS1_OAEP.new(recipient_key)
outfile = "encrypted_"+str(send_node)+ "_data.bin"
print "outfile=", outfile
file_out = open(outfile, "wb")
file_out.write(cipher_rsa.encrypt(session_key))

# Encrypt the data with the AES session key
cipher_aes = AES.new(session_key, AES.MODE_EAX)
ciphertext, tag = cipher_aes.encrypt_and_digest(data)
[ file_out.write(x) for x in (cipher_aes.nonce, tag, ciphertext) ]


