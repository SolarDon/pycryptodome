I created these examples to get you started.  If you have questions or comments send them to crypto@sol-solution.net
Don

To start you can run Test.bat
if not before you start please create the keys subdirectory and you will probalby want to run these in this order

Test.bat - runs tests with default, using optional settings and testing error conditions

GenerateRSAKeys.py - Generate public and private keys for nodes 0-7

EncryptData.py - optional parameters
                    node=<node_number>  between 0 and 7
                    message=<message>
                 Will encrypt the message

DecryptData.py - optional parameters
                    node=<node_number>  between 0 and 7
                 Will decrypt the message

SignVerify.py - Example of signing and verifies a message

Sign.py - optional parameters
              node=<node_number>  between 0 and 7
              message=<message>
          Will sign a message

Verify.py - optional parameters
               node=<node_number>  between 0 and 7
               message=<message>
            Will verify a message

SignEncrypt.py - optional parameters
               send=<send_node_number>  between 0 and 7
               recv=<recv_node_number>  between 0 and 7
               message=<message>
     This is to sign a document then encypt it.
     This allows only the reciever can decrypt the data and that the data is from a verified source
     The file will be written to encrypted_<send_node>_data.bin


DecryptVerify.py - optional parameters
               send=<send_node_number>  between 0 and 7
               recv=<recv_node_number>  between 0 and 7
      This decryts then verifies a signed and encypted data.
      This allows only the reciever can decrypt the data and that the data is from a verified source
      The file will be read from encrypted_<send_node>_data.bin