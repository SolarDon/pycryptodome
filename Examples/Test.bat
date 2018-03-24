REM clean up old keys if they exist
del /Q keys
rmdir keys
mkdir keys
rm *.bin

@echo Generate keys
python GenerateRSAKeys.py

python EncryptData.py
python DecryptData.py

@echo simulate decryption failure
python DecryptData.py node=7

rem has sign and verify in the same file
python SignVerify.py

python Sign.py
python Verify.py
python Sign.py node=5 message="Summer was fun"
python Verify.py node=5 message="Summer was fun"
rem simulate failure
python Verify.py node=4 message="Summer was fun"
python Verify.py node=5 message="Summer was bad"

rem Has Sign and Verify in one file
python SignVerify.py

rem check defaults (send=1 recv=2)
python SignEncrypt.py
python DecryptVerify.py

# Will create then use encrypted_4_data.bin
python SignEncrypt.py send=4 recv=5 message="Summer was fun"
python DecryptVerify.py send=4 recv=5

@echo Simulate sending to the wrong node
python DecryptVerify.py  send=4 recv=6

echo The sent node information is in the date so we
copy  encrypted_4_data.bad encrypted_4_data.bin
python DecryptVerify.py send=4 recv=5