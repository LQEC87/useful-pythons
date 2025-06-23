import math
import sys

from typing import Callable, Literal

from uuid import getnode as _getnode
from socket import gethostname as _gethostname, gethostbyname as _gethostbyname

def tetration(a:int, n:int):
    t = 1
    for _ in range(n):
        t = a ** t
    return t

def logn(a,n):
    if(n==None):
        return math.log(a)
    return math.log(a)/math.log(n)

def digits(n):
    return int(math.log10(n))+1

def intstrlen(n:int):
    return len(str(abs(n)))

def easyintlog2(n:int) -> int:
    return n.bit_length()-1

def intdigits(n:int) -> int:
    if sys.float_info.max<n:
        dig = 1
        lbn = easyintlog2(n)
        while(dig*math.log2(10)<lbn):
            dig += 1
        return dig-1
    else:
        dig = 1
        while(10**dig<=n):
            dig += 1
        return dig-1

def intdivision(n:int,m:int) -> int:
    return int(n // m + (0 if n%m*10/m<5 else 1))

def intlog10(n:int) -> int:
    idig = intdigits(n)
    if(idig-sys.float_info.max_10_exp+digits(math.log2(10))<0):
        return intdivision(easyintlog2(n)*(10**idig),int(math.log2(10)*(10**idig)))
    return intdivision(easyintlog2(n)*(10**idig),int(math.log2(10)*10**(sys.float_info.max_10_exp-digits(math.log2(10))))*int(10**(idig-sys.float_info.max_10_exp+digits(math.log2(10)))))

def myaboutlog10accuracy(n:float):
    if n==1:
        return 100
    return (intlog10(int(n))-math.log10(n))/math.log10(n)*100

def brlog10(n): # log10 selector for big range of n
    if(type(n)==float):
        return math.log10(n)
    elif(type(n)==int):
        if(intlog10(n)<(10**sys.float_info.max_10_exp)):
            return math.log10(n)
        else:
            return intlog10(int(n))
    else:
        return None

def clearconsole():
    for _ in range(10000):
        print("\n",end="")
    return print((0).to_bytes().decode())

"""hexing - Which do you use??
>>> byte = b"\xab\xcd\xef"
>>> byte.hex()
'abcdef'
>>> import binascii
>>> binascii.hexlify(byte)
b'abcdef'
>>> str(binascii.hexlify(byte), 'utf-8')
'abcdef'
>>> str(binascii.b2a_hex(byte), 'utf-8')
'abcdef'

>>> string = "abcdef"
>>> bytes.fromhex(string)
b'\xab\xcd\xef'
>>> import binascii
>>> binascii.unhexlify(string)
b'\xab\xcd\xef'
>>> binascii.a2b_hex(string)
b'\xab\xcd\xef'
>>> binascii.hexlify(binascii.unhexlify(string) *OR* bytes.fromhex(string))
b'abcdef'


READ THE DOC
https://qiita.com/masakielastic/items/21ba9f68ef6c4fd7692d
"""

def xorhash(hash1,hash2):
    return hex(int(hash1,base=16)^int(hash2,base=16))[2:]

def UTF8num(string:str) -> int:
    return int.from_bytes(string.encode("utf-8"))
def numUTF8(num:int) -> str:
    return get_bytes(num).decode("utf-8")
def get_bytes(num:int, byteorder: Literal['little', 'big'] = "big",*, signed: bool = False) -> bytes:
    return num.to_bytes((num.bit_length()+7)//8, byteorder=byteorder, signed=signed)

def slit(string:str,wide:int) -> list:
    return [string[i:i+wide] for i in range(0,len(string),wide)]

def macaddress():
    return ":".join(slit(hex(_getnode())[2:],2))
def ipaddress():
    return _gethostbyname(_gethostname())

def my_function_call_function(input,func:Callable):
    return func(input)

from platform import python_version_tuple
if int(python_version_tuple()[0])>=3 and int(python_version_tuple()[1])>=13:
    from typing_extensions import deprecated
    @deprecated("Too small to stop code.")
    def q():
        quit()
else:
    from warnings import warn
    def q():
        warn("Too small to stop code.",DeprecationWarning)
        quit()

if __name__ == "__main__":
    print("Hello, World!")