from sys import exit, argv
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5

'''
This decryts then verifies a signed and encypted data.
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
        else:
            print "Invalid input, valid inputs are\n\tsend=<send_node>\n\trecv=<recv_node"
            exit(1)            

file_name="encrypted_"+str(send_node)+ "_data.bin"
print "file_name=", file_name
file_in = open(file_name, "rb")
#recv_private_key_file = "keys\N"+str(recv_node)+"_private_key"
recv_private_key_data = open("keys\N"+str(recv_node)+"_private_key").read()
secret_code = "Node" + str(recv_node)
print "secret_code=", secret_code
private_key = RSA.import_key(recv_private_key_data, passphrase=secret_code )

enc_session_key, nonce, tag, ciphertext = \
   [ file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1) ]

# Decrypt the session key with the public RSA key
cipher_rsa = PKCS1_OAEP.new(private_key)
session_key = cipher_rsa.decrypt(enc_session_key)

# Decrypt the data with the AES session key
cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
data = cipher_aes.decrypt_and_verify(ciphertext, tag)
print(data)
signature = data[0:128]
node = data[128]
message = data[129:]
print "node=", node
print message

# Now verify the data
secret_code = "Node" + str(send_node)
print secret_code
public_key = RSA.import_key(open("keys\N" + str(node) + "_public_key").read(), passphrase=secret_code )
digest = SHA256.new(message)
try:
   verifier = PKCS1_v1_5.new(public_key.publickey())
   verified = verifier.verify(digest, signature)
   assert verified, 'Signature verification failed'
   print "The signature is valid."
except (ValueError, TypeError):
   print "The signature is not valid."
