from Encryptions import AES,RSA
from useful_functions import anyfunction as af

# Encrypt Example
AES.encryption.key_length = 32

data = "test text".encode("utf-8")

aeskey = AES.encryption.keygen()
enc1 = AES.encryption(aeskey, data=data)
enc1.encrypter()

ciphertext = enc1.ct
initiationvector = enc1.iv

private_key, public_key = RSA.encryption.eskeygen()
enc2 = RSA.encryption(None, public_key, data=aeskey)
enc2.encrypter()

cipheredkey = enc2.ct

enc3 = RSA.encryption(private_key, None, ciphertext=cipheredkey)
enc3.decrypter()

decryptedkey = enc3.data

enc4 = AES.encryption(decryptedkey, initiationvector, ciphertext)
enc4.decrypter()

print(f"Hybrid Encryption> data:{enc4.data}")

# Lot of function is here
tet3_3 = af.tetration(3, 3) # 3↑↑3 = 3↑3↑3 = 3^3^3
print(f"{af.intlog10(tet3_3)=}")
print(f"{af.UTF8num("a")=}")
print(f"{af.get_bytes(42)=}")