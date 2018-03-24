from sys import exit, argv
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

# first set defaults
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
        elif variable == "message":
            message = value
print "node=", node
public_key = RSA.import_key(open("keys\N" + str(node) + "_public_key").read(), passphrase= "Node"+str(node) )
digest = SHA256.new(message)
print message
print digest

file_in = open("sig.bin", "rb")
signature=file_in.read()
print signature

try:
   verifier = PKCS1_v1_5.new(public_key.publickey())
   verified = verifier.verify(digest, signature)
   assert verified, 'Signature verification failed'
   print "The signature is valid."
except (ValueError, TypeError):
   print "The signature is not valid."
