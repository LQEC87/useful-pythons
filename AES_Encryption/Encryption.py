# -*- coding: UTF-8 -*-
"""AES(CBC Mode) Compacts

You can encrypt easily!
This package contains Easy encryption programs!

Examples:

  >>> from Encryption import encryption
  >>> key = encryption.keygen()
  >>> enc = encryption(key, data="password")
  >>> enc.encrypter()
  >>> enc.iv
  b"somerandombytesobject"
  >>> enc.ct
  b"0encryptedbytesobject"


"""
from base64 import b64encode,b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import warnings

class NoSetKeyWarning(UserWarning):
    "not setting key warnings based by :obj:`UserWarning`"
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class encryption:
    """Easy to encrypt data with AES system.

    AESでの暗号化を簡単に行うためのラッパーです。
    クラスのメソッドを直線呼び出すことができますが、
    インスタンス作成時に設定することもできます。
    インスタンス化する際は必ずキーを入力してください。

    Wrapper for easy encryption with AES.
    You can call methods of the class in a straight line,
    or you can set them at instantiation time.
    Be sure to enter the key when instantiating.

    Attributes:
      aes_block_size (int) : AES fixed length.
      key_length (int) : Key length required for this module.
    """
    aes_block_size : int = AES.block_size #! only copy data: 16bytes
    key_length : int = AES.block_size # needed key lengths : 16bytes

    def __init__(self,key:bytes,iv:bytes|None=None,ct:bytes|None=None,data:bytes|None=None):
        """Initializes the instance based on input infomations.

        You should input `key` or warn :obj:`NoSetKeyWarning` and automate setkey.

        Args:
            key (bytes) : set key, Be sure to enter the key when instantiating.
            iv (bytes) : initiation vector
            ct (bytes) : ciphered text
            data (bytes) : plain data
        """
        for arg_name,arg in locals().items():
            if arg_name in ["key","iv","ct","data"] and not isinstance(arg,bytes) and arg!=None:
                raise TypeError(f"{arg_name} is not bytes")
        if len(key)!=encryption.key_length:
            warnings.warn("you should set proper key yourself",category=NoSetKeyWarning)
            key = self.setkey()
        else:
            self.key = key
        self.iv = iv
        self.ct = ct
        self.data = data
        return
    
    @classmethod
    def keygen(cls):
        "AES key generator"
        return get_random_bytes(cls.key_length)
    def setkey(self):
        "sets key to myself"
        self.key = self.keygen()
        return self.key

    @staticmethod
    def encrypt(key:bytes, data:bytes, iv:bytes|None=None) -> tuple[bytes, bytes]:
        """Encrypt data with key and iv.
        
        Args:
          key (byte string) : It's :data:`key_length` sized bytes.
          data (byte string) : Some bytes-typed data.
          iv (byte string, optional) : :data:`aes_block_size` sized bytes, but if None, auto generated.
        
        Returns:
          (iv,ct) (tuple[byte string, byte string]) : Initialization Vector, and Cipher Text.
        """
        
        if iv==None:
            cipher = AES.new(key, AES.MODE_CBC)
        else:
            cipher = AES.new(key, AES.MODE_CBC, iv)
        ct_bytes = cipher.encrypt(pad(data,AES.block_size))
        return bytes(cipher.iv),ct_bytes
    def encrypter(self):
        if self.data!=None:
            self.iv,self.ct = self.encrypt(self.key,self.data,self.iv)
            return (self.iv,self.ct)
        else:
            self.iv,self.ct = self.encrypt(self.key,bytes(0),self.iv)
            return (self.iv,self.ct)

    @staticmethod
    def decrypt(key:bytes, iv:bytes, ct:bytes) -> bytes:
        """Decrypt ct with key and iv.
        
        Args:
          key (byte string) : Key bytes, :data:`key_length` sized bytes.
          iv (byte string) : Initialization vector, :data:`aes_block_size` sized bytes.
          ct (byte string) : Cipher text, bytes-typed encrypted data.
        
        Returns:
          data (byte string) : Decrypted bytes-typed data.
        """
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ct), AES.block_size)
    def decrypter(self):
        if self.key!=None and self.iv!=None and self.ct!=None:
            self.data = self.decrypt(self.key,self.iv,self.ct)
            return self.data
        else:
            return None

    @classmethod
    def bstr(cls,b:bytes):
        return (("0"*2*len(b))+hex(int.from_bytes(b))[2:])[-(2*len(b)):]
    @classmethod
    def _bprint(cls,b:bytes):
        print(cls.bstr(b))
        return

class b64encryption(encryption):
    """Base64 version of :obj:`encryption`

    :obj:`encryption` with Base64 encoding,
    but there are a few changes in the system.
    """

    b64aes_block_size : int = len(b64encode((0).to_bytes(AES.block_size)))
    b64key_length : int = len(b64encode((0).to_bytes(AES.block_size)))

    def __init__(self,key:str,iv:str|None=None,ct:str|None="",data:str|None=""):
        for arg_name,arg in locals().items():
            if arg_name in ["key","iv","ct","data"] and not isinstance(arg,str) and arg!=None:
                raise TypeError(f"{arg_name} is not str")
        if len(key)!=self.b64key_length or len(b64decode(key))!=super().key_length:
            warnings.warn("you should set proper key yourself",category=NoSetKeyWarning)
            key = self.setkey()
        else:
            self.key = key
        self.iv = iv # only Noneable
        self.ct = ct
        self.data = data
        return
    
    @classmethod
    def keygen(cls,encoding:str="utf-8"):
        # If I use super().keygen() here, b64's key_length will be called.
        return b64encode(get_random_bytes(AES.block_size)).decode(encoding)
    def setkey(self,encoding:str="utf-8"):
        self.key = self.keygen(encoding=encoding)
        return self.key

    @staticmethod
    def encrypt(key:str, data:str, data_encoding : str = 'utf-8', output_encoding:str='utf-8', iv:str|None=None):
        """Encrypt data with key and iv.
        
        Args:
          key (base64 string) : It's :data:`key_length` sized bytes of base64 string.
          data (string)  : Some string data.
          iv (base64 string, optional) : :data:`aes_block_size` sized bytes of base64 string, but if None, auto generated.
        
        Returns:
          (iv,ct) (tuple[base64 string, base64 string]) : Initialization Vector, and Cipher Text.
        """
        bkey:bytes = b64decode(key)
        bdata:bytes = data.encode(encoding=data_encoding)
        if iv==None:
            biv,ct = encryption.encrypt(bkey,bdata)
        else:
            biv = b64decode(iv)
            _,ct = encryption.encrypt(bkey,bdata,biv)
        iv,ct = b64encode(biv).decode(encoding=output_encoding),b64encode(ct).decode(encoding=output_encoding)
        return iv,ct
    def encrypter(self):
        if self.data is not None:
            self.iv,self.ct = self.encrypt(self.key,self.data)
        else:
            self.iv,self.ct = self.encrypt(self.key,"")
        return self.iv,self.ct
    
    @staticmethod
    def decrypt(key:str, iv:str, ct:str, encoding:str='utf-8'):
        """Decrypt ct with key and iv.
        
        Args:
          key (base64 string) : Key string, :data:`key_length` sized bytes of base64 string.
          iv (base64 string) : Initialization vector, :data:`aes_block_size` sized bytes of base64 string.
          ct (base64 string) : Cipher text, encrypted data of base64 string.
        
        Returns:
          data (string) : Decrypted data.
        """
        bkey,biv,bct = b64decode(key),b64decode(iv),b64decode(ct)
        return encryption.decrypt(bkey,biv,bct).decode(encoding=encoding)
    def decrypter(self):
        if self.iv is not None and self.ct is not None:
            self.data = self.decrypt(self.key,self.iv,self.ct)
            return self.data
        else:
            return None

    @classmethod
    @warnings.deprecated("this func is not for b64")
    def bstr(cls, b):
        "this func is not for b64"
        return super().bstr(b)
    @classmethod
    @warnings.deprecated("this func is not for b64")
    def _bprint(cls, b):
        "this func is not for b64"
        return super()._bprint(b)
    


if __name__=="__main__":
    data = "password"
    print(f"plaintext:{data}")
    print("encode by utf-8")
    encryption._bprint(data.encode())
    #bytes encryption
    from os import urandom
    key = urandom(encryption.key_length)
    enc1 = encryption(urandom(encryption.key_length),data=data.encode())
    enc1.encrypter()
    print("iv")
    encryption._bprint(enc1.iv or bytes())
    print("ct")
    encryption._bprint(enc1.ct or bytes())
    enc1.decrypter()
    print("decoded data")
    encryption._bprint(enc1.data or bytes())
    print(f"decode by utf-8:{(enc1.data or bytes()).decode()}") # f**k
    print()
    #base64 encryption
    bkey = b64encode(key).decode("utf-8")
    enc2 = b64encryption(bkey,data=data)
    enc2.encrypter()
    print("iv")
    print(enc2.iv)
    print("ct")
    print(enc2.ct)
    enc2.decrypter()
    print("decrypted data")
    print(enc2.data)
    print()
    print("more easy!")