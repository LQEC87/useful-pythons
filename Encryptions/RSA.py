# -*- coding: UTF-8 -*-

from typing import Literal
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import warnings
from EncWarn import NoSetKeyWarning

class encryption:
    key_length = 2048
    def __init__(self,private_key:bytes|None,public_key:bytes|None,data:bytes=b"",ciphertext:bytes=b"") -> None:
        if private_key is None and public_key is None:
            warnings.warn("you should set proper key yourself",category=NoSetKeyWarning)
            private_key,public_key = self.eskeygen()
        if len(data)>190:
            warnings.warn("data length is longer than 190bytes. this may not able to encrypt.")
        self.priKey = private_key or b""
        self.pubKey = public_key or b""
        self.data = data
        self.ct = ciphertext
    @classmethod
    def eskeygen(cls):
        "Return (PrivateKey,PublicKey)"
        key = RSA.generate(cls.key_length)
        priKey = key.export_key("DER")
        pubKey = key.public_key().export_key("DER")
        return priKey,pubKey
    @classmethod
    def keygen(cls,passphrase:str,pkcs:int|None=1,protection:str|None=None,randfunc=None):
        key = RSA.generate(cls.key_length)
        priKey = key.export_key("DER",passphrase,pkcs,protection,randfunc)
        pubKey = key.public_key().export_key("DER")
        return priKey,pubKey
    def getKey(self):
        private_key = self.priKey.hex()
        public_key = self.pubKey.hex()
        return private_key,public_key
    def getData(self):
        datahexed = self.data.hex()
        cipherdatahexed = self.ct.hex()
        return datahexed,cipherdatahexed
    @staticmethod
    def convKey(rsakey:bytes, format:Literal["PEM","DER","OpenSSH"]|None="PEM"):
        key = RSA.import_key(rsakey)
        return key.export_key(format=format)
    def getPEMKey(self):
        return self.convKey(self.priKey,"PEM"),self.convKey(self.pubKey,"PEM")
    @staticmethod
    def encrypt(public_key:bytes, data:bytes, **kwargs):
        pubkey = RSA.import_key(public_key)
        if kwargs != {}:
            cipher = PKCS1_OAEP.new(pubkey, **kwargs)
        else:
            cipher = PKCS1_OAEP.new(pubkey)
        encrypted = cipher.encrypt(data)
        return encrypted
    def encrypter(self):
        self.ct = self.encrypt(self.pubKey,self.data)
        return self.ct
    @staticmethod
    def decrypt(private_key:bytes, ciphertext:bytes, **kwargs):
        prikey = RSA.import_key(private_key)
        if kwargs != {}:
            cipher = PKCS1_OAEP.new(prikey, **kwargs)
        else:
            cipher = PKCS1_OAEP.new(prikey)
        decrypted = cipher.decrypt(ciphertext)
        return decrypted
    def decrypter(self):
        self.data = self.decrypt(self.priKey,self.ct)
        return self.data
    
if __name__ == "__main__":
    NoSetKeyWarning.ignore()
    enc = encryption(None,None,data="password".encode())
    print("privateKey, publicKey")
    gotkey = enc.getKey()
    print(gotkey)
    enc.encrypter()
    print("plain, ciphered")
    gotdata = enc.getData()
    print(gotdata)
    decrypteddata = encryption.decrypt(enc.priKey,enc.ct)
    print()
    print("decrypted")
    print(decrypteddata)