from sys import exit, argv
from Crypto.Signature import pkcs1_15
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

# Read private key from file
private_key = RSA.import_key(open("keys\N" + str(node) + "_private_key").read(), passphrase= "Node"+str(node))
digest = SHA256.new(message)
signature = pkcs1_15.new(private_key).sign(digest)
print signature
file_out = open("sig.bin", "wb")
file_out.write(signature)
