from sys import exit, argv
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA

send_node = 1
recv_node = 2
message = "Signed data from SignVerify.py"

if __name__ == "__main__":
    for my_args in argv[1:]:
        variable,value = my_args.split('=')
        if variable == "recv" :
            node =int(value)
            if node > 7 or node < 0:
                print "node needs to be between 0 and 7"
                exit(1)
        elif variable == "send" :
            node =int(value)
            if node > 7 or node < 0:
                print "node needs to be between 0 and 7"
                exit(1)                
        elif variable == "message":
            message = value

# Read private key from file
with open ("keys\N" + str(node) + "_private_key", "rb") as myfile:    
    private_key = RSA.importKey(myfile.read(), passphrase="Node"+str(node))

# Load private key and sign message
digest = SHA256.new(message)
sig = PKCS1_v1_5.new(private_key).sign(digest)

# Can simulate failure by changing message or node
#message = "Different Message"
#digest = SHA256.new(message)
#node = 7

# Load public key and verify message
with open ("keys\N" + str(node) + "_public_key", "rb") as myfile:
    public_key = RSA.importKey(myfile.read(), passphrase="Node"+str(node))
verifier = PKCS1_v1_5.new(public_key.publickey())
verified = verifier.verify(digest, sig)
assert verified, 'Signature verification failed'
print 'Successfully verified message'
