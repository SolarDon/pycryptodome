from Crypto.PublicKey import RSA

'''
Generate public and private keys for nodes 0-7
'''
# from http://pycryptodome.readthedocs.io/en/latest/src/examples.html
node_str=""
for i in range(0,8):
    secret_code = "Node" + str(i)
    node_str += secret_code + " "
    key = RSA.generate(1024)
    encrypted_key = key.exportKey(passphrase=secret_code, pkcs=8 )
    file_name = "keys\N"+str(i)+"_private_key"
    file_out = open(file_name, "wb")
    file_out.write(encrypted_key)
    file_out.close
    public_name = "keys\N"+str(i)+"_public_key"
    public_file = open(public_name, "wb")
    public_file.write(key.publickey().exportKey())
    #print(key.publickey().exportKey())
    public_file.close()
print "Keys generated for: ", node_str
