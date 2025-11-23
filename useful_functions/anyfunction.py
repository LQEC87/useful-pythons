import sys as _sys
import os as _os
import time as _time
import datetime as _datetime
import math as _math
import random as _random
from decimal import Decimal as _Decimal
from fractions import Fraction as _Fraction
from enum import Enum as _Enum
from typing import Any as _Any, Callable as _Callable, Literal as _Literal, LiteralString as _LiteralString, SupportsFloat as _SupportsFloat, Type as _Type
from itertools import chain as _chain, count as _count
from collections import deque as _deque

from uuid import getnode as _getnode
from socket import gethostname as _gethostname, gethostbyname as _gethostbyname

from copy import deepcopy as _deepcopy

from warnings import warn as _warn, catch_warnings as _catch_warnings
from platform import python_version_tuple as _python_version_tuple

class Calcurations:
    
    primes = [2]

    def __init__(self):
        self.PI = self.pi(self.piCalcurator.RAMANUJAN,10)
        self.E = self.e()

    class piCalcurator(_Enum):
        RAMANUJAN = 0
        MONTECARLO = 1
        LEIBNIZ = 2
        TRAPEZOIDALRULE = 3
        WALLISPRODUCT = 4
        RAMANUJAN1914 = 5
        CHUDNOVSKY = 6
        BORWEIN = 7
        GAUSSLEGENDRE = 8
        EULER = 9
        BAILEYBORWEINPLOUFFE = 10
        BELLARD = 11
        高野喜久雄 = 314
    
    @staticmethod
    def fibonatti(n:int, fast:bool=False):
        if fast:
            r5 = _math.sqrt(5)
            return int((1/r5) * (((1+r5)/2)**n - ((1-r5)/2)**n))
        a = 0
        b = 1
        for _ in range(n):
            a,b = b,a+b
        return b
    
    @staticmethod
    def tetration(a:int, n:int):
        "a↑↑n = a^a^a^a^...}←n times"
        t = 1
        for _ in range(n):
            t = a ** t
        return t
    
    @classmethod
    def ackermann(cls, m:int, n:int) -> int:
        "ackermann function. if you don't know what it was, you should google it."
        if n<0 or m<0:
            raise ValueError("n and m must be positive numbers.")
        if m==0:
            return n+1
        if n==0:
            return cls.ackermann(m-1,1)
        #_warn("This function creates huge recursion.",RecursionWarning)
        with _catch_warnings(action="always",category=ResourceWarning): # ResourceWarning is set default to "ignore"
            _warn("This function creates huge recursion.", ResourceWarning)
        return cls.ackermann(m-1, cls.ackermann(m, n-1))
    
    @staticmethod
    def f_root(a:_Fraction,N:int):
        "sqrt(a)"
        if a == _Fraction(0):
            return _Fraction(0)
        sign = -1 if a < 0 else 1
        b = _Fraction(a*sign)
        if b>10**5:
            try:
                b = _Fraction(_math.sqrt(b))
            except OverflowError:
                try:
                    b = _Fraction(_math.log(b.numerator)-_math.log(b.denominator))
                except OverflowError:
                    b = _Fraction(b.numerator.bit_length()-b.denominator.bit_length())
        for _ in range(N):
            b = (a + b*b)/(b*2)
        return b*sign
    
    @staticmethod
    def aF_powby_bI(a:_Fraction,b:int):
        a,b = _Fraction(a), int(b)
        return _Fraction(a.numerator**b,a.denominator**b)
    @classmethod
    def aI_root_bF(cls, a:int,b:_Fraction,N:int, LIMITS:int=0):
        # x=b^n(1-n)-a / nb^(n-1)
        # y=at^(a-1)x+t^a(1-a)-b
        # x = t^a(1-a)-b / at^(a-1)
        a,b = int(a), _Fraction(b)
        if a<=0:
            raise ValueError("a must be greater than 0")
        if a==1:
            return b
        if b==0:
            return _Fraction(0)
        try:
            ans = _Fraction(_math.pow(b,1/a))
        except OverflowError:
            ans = cls.f_root(b,N)/a
        for _ in range(N):
            ans = (cls.aF_powby_bI(ans, a)*(1-a)-b)/(a*cls.aF_powby_bI(ans, a-1))
            if LIMITS>0:
                ans = ans.limit_denominator(LIMITS)
        return ans
    @classmethod
    def powFraction(cls, a:_Fraction,b:_Fraction,N:int, LIMITS:int=0):
        # a^b = (p/q)^(r/s) = p^(r/s)/q^(r/s) ≠ (p^r)*s√p / (q^r)*s√q = p^r/q^r * s√(p/q)
        # !!!!!!!!!!!!!!!!ERROR!!!!!!!!!!!!!!!!!!!!
        # nb^(n-1)x+b^n(1-n)-a
        # a^b = (p/q)^(r/s) = p^(r/s)/q^(r/s) = s√(p^r) / s√(q^r) = s√(p^r/q^r) = s√((p/q)^r)
        a,b = _Fraction(a),_Fraction(b)
        return cls.aI_root_bF(b.denominator, cls.aF_powby_bI(a,b.numerator), N, LIMITS) if LIMITS>0 else cls.aI_root_bF(b.denominator, cls.aF_powby_bI(a,b.numerator), N)
    @classmethod
    def powBinFract(cls, b:_Fraction,N:int, LIMITS:int=0):
        "2^`b`"
        # 2^b = 2^(r/s) = s√(2^r)
        b=_Fraction(b)
        return cls.aI_root_bF(b.denominator, _Fraction(1 << b.numerator),N,LIMITS) if LIMITS>0 else cls.aI_root_bF(b.denominator, _Fraction(1 << b.numerator),N)
    
    @classmethod
    def isprime(cls, n:int, speed:int=-1):
        if n<=1:
            raise ValueError("`n` must be greater than 1")
        match speed:
            case 0:
                for i in range(2,n):
                    if n%i==0:
                        return False
                return True
            case 1:
                for i in range(2,n//2):
                    if n%i==0:
                        return False
                return True
            case 2:
                for i in range(2,_math.ceil(_math.sqrt(n))+1):
                    if n%i==0:
                        return False
                return True
            case 3:
                if n%2==0:
                    return False
                for i in range(3,_math.ceil(_math.sqrt(n))+1,2):
                    if n%i==0:
                        return False
                return True
            case 4:
                smallprimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063, 1069, 1087, 1091, 1093, 1097, 1103, 1109, 1117, 1123, 1129, 1151, 1153, 1163, 1171, 1181, 1187, 1193, 1201, 1213, 1217, 1223, 1229, 1231, 1237, 1249, 1259, 1277, 1279, 1283, 1289, 1291, 1297, 1301, 1303, 1307, 1319, 1321, 1327, 1361, 1367, 1373, 1381, 1399, 1409, 1423, 1427, 1429, 1433, 1439, 1447, 1451, 1453, 1459, 1471, 1481, 1483, 1487, 1489, 1493, 1499, 1511, 1523, 1531, 1543, 1549, 1553, 1559, 1567, 1571, 1579, 1583, 1597, 1601, 1607, 1609, 1613, 1619, 1621, 1627, 1637, 1657, 1663, 1667, 1669, 1693, 1697, 1699, 1709, 1721, 1723, 1733, 1741, 1747, 1753, 1759, 1777, 1783, 1787, 1789, 1801, 1811, 1823, 1831, 1847, 1861, 1867, 1871, 1873, 1877, 1879, 1889, 1901, 1907, 1913, 1931, 1933, 1949, 1951, 1973, 1979, 1987, 1993, 1997, 1999, 2003, 2011, 2017, 2027, 2029, 2039, 2053, 2063, 2069, 2081, 2083, 2087, 2089, 2099, 2111, 2113, 2129, 2131, 2137, 2141, 2143, 2153, 2161, 2179, 2203, 2207, 2213, 2221, 2237, 2239, 2243, 2251, 2267, 2269, 2273, 2281, 2287, 2293, 2297, 2309, 2311, 2333, 2339, 2341, 2347, 2351, 2357, 2371, 2377, 2381, 2383, 2389, 2393, 2399, 2411, 2417, 2423, 2437, 2441, 2447, 2459, 2467, 2473, 2477, 2503, 2521, 2531, 2539, 2543, 2549, 2551, 2557, 2579, 2591, 2593, 2609, 2617, 2621, 2633, 2647, 2657, 2659, 2663, 2671, 2677, 2683, 2687, 2689, 2693, 2699, 2707, 2711, 2713, 2719, 2729, 2731, 2741, 2749, 2753, 2767, 2777, 2789, 2791, 2797, 2801, 2803, 2819, 2833, 2837, 2843, 2851, 2857, 2861, 2879, 2887, 2897, 2903, 2909, 2917, 2927, 2939, 2953, 2957, 2963, 2969, 2971, 2999, 3001, 3011, 3019, 3023, 3037, 3041, 3049, 3061, 3067, 3079, 3083, 3089, 3109, 3119, 3121, 3137, 3163, 3167, 3169, 3181, 3187, 3191, 3203, 3209, 3217, 3221, 3229, 3251, 3253, 3257, 3259, 3271, 3299, 3301, 3307, 3313, 3319, 3323, 3329, 3331, 3343, 3347, 3359, 3361, 3371, 3373, 3389, 3391, 3407, 3413, 3433, 3449, 3457, 3461, 3463, 3467, 3469, 3491, 3499, 3511, 3517, 3527, 3529, 3533, 3539, 3541, 3547, 3557, 3559, 3571, 3581, 3583, 3593, 3607, 3613, 3617, 3623, 3631, 3637, 3643, 3659, 3671, 3673, 3677, 3691, 3697, 3701, 3709, 3719, 3727, 3733, 3739, 3761, 3767, 3769, 3779, 3793, 3797, 3803, 3821, 3823, 3833, 3847, 3851, 3853, 3863, 3877, 3881, 3889, 3907, 3911, 3917, 3919, 3923, 3929, 3931, 3943, 3947, 3967, 3989, 4001, 4003, 4007, 4013, 4019, 4021, 4027, 4049, 4051, 4057, 4073, 4079, 4091, 4093, 4099, 4111, 4127, 4129, 4133, 4139, 4153, 4157, 4159, 4177, 4201, 4211, 4217, 4219, 4229, 4231, 4241, 4243, 4253, 4259, 4261, 4271, 4273, 4283, 4289, 4297, 4327, 4337, 4339, 4349, 4357, 4363, 4373, 4391, 4397, 4409, 4421, 4423, 4441, 4447, 4451, 4457, 4463, 4481, 4483, 4493, 4507, 4513, 4517, 4519, 4523, 4547, 4549, 4561, 4567, 4583, 4591, 4597, 4603, 4621, 4637, 4639, 4643, 4649, 4651, 4657, 4663, 4673, 4679, 4691, 4703, 4721, 4723, 4729, 4733, 4751, 4759, 4783, 4787, 4789, 4793, 4799, 4801, 4813, 4817, 4831, 4861, 4871, 4877, 4889, 4903, 4909, 4919, 4931, 4933, 4937, 4943, 4951, 4957, 4967, 4969, 4973, 4987, 4993, 4999, 5003, 5009, 5011, 5021, 5023, 5039, 5051, 5059, 5077, 5081, 5087, 5099, 5101, 5107, 5113, 5119, 5147, 5153, 5167, 5171, 5179, 5189, 5197, 5209, 5227, 5231, 5233, 5237, 5261, 5273, 5279, 5281, 5297, 5303, 5309, 5323, 5333, 5347, 5351, 5381, 5387, 5393, 5399, 5407, 5413, 5417, 5419, 5431, 5437, 5441, 5443, 5449, 5471, 5477, 5479, 5483, 5501, 5503, 5507, 5519, 5521, 5527, 5531, 5557, 5563, 5569, 5573, 5581, 5591, 5623, 5639, 5641, 5647, 5651, 5653, 5657, 5659, 5669, 5683, 5689, 5693, 5701, 5711, 5717, 5737, 5741, 5743, 5749, 5779, 5783, 5791, 5801, 5807, 5813, 5821, 5827, 5839, 5843, 5849, 5851, 5857, 5861, 5867, 5869, 5879, 5881, 5897, 5903, 5923, 5927, 5939, 5953, 5981, 5987, 6007, 6011, 6029, 6037, 6043, 6047, 6053, 6067, 6073, 6079, 6089, 6091, 6101, 6113, 6121, 6131, 6133, 6143, 6151, 6163, 6173, 6197, 6199, 6203, 6211, 6217, 6221, 6229, 6247, 6257, 6263, 6269, 6271, 6277, 6287, 6299, 6301, 6311, 6317, 6323, 6329, 6337, 6343, 6353, 6359, 6361, 6367, 6373, 6379, 6389, 6397, 6421, 6427, 6449, 6451, 6469, 6473, 6481, 6491, 6521, 6529, 6547, 6551, 6553, 6563, 6569, 6571, 6577, 6581, 6599, 6607, 6619, 6637, 6653, 6659, 6661, 6673, 6679, 6689, 6691, 6701, 6703, 6709, 6719, 6733, 6737, 6761, 6763, 6779, 6781, 6791, 6793, 6803, 6823, 6827, 6829, 6833, 6841, 6857, 6863, 6869, 6871, 6883, 6899, 6907, 6911, 6917, 6947, 6949, 6959, 6961, 6967, 6971, 6977, 6983, 6991, 6997, 7001, 7013, 7019, 7027, 7039, 7043, 7057, 7069, 7079, 7103, 7109, 7121, 7127, 7129, 7151, 7159, 7177, 7187, 7193, 7207, 7211, 7213, 7219, 7229, 7237, 7243, 7247, 7253, 7283, 7297, 7307, 7309, 7321, 7331, 7333, 7349, 7351, 7369, 7393, 7411, 7417, 7433, 7451, 7457, 7459, 7477, 7481, 7487, 7489, 7499, 7507, 7517, 7523, 7529, 7537, 7541, 7547, 7549, 7559, 7561, 7573, 7577, 7583, 7589, 7591, 7603, 7607, 7621, 7639, 7643, 7649, 7669, 7673, 7681, 7687, 7691, 7699, 7703, 7717, 7723, 7727, 7741, 7753, 7757, 7759, 7789, 7793, 7817, 7823, 7829, 7841, 7853, 7867, 7873, 7877, 7879, 7883, 7901, 7907, 7919, 7927, 7933, 7937, 7949, 7951, 7963, 7993, 8009, 8011, 8017, 8039, 8053, 8059, 8069, 8081, 8087, 8089, 8093, 8101, 8111, 8117, 8123, 8147, 8161, 8167, 8171, 8179, 8191, 8209, 8219, 8221, 8231, 8233, 8237, 8243, 8263, 8269, 8273, 8287, 8291, 8293, 8297, 8311, 8317, 8329, 8353, 8363, 8369, 8377, 8387, 8389, 8419, 8423, 8429, 8431, 8443, 8447, 8461, 8467, 8501, 8513, 8521, 8527, 8537, 8539, 8543, 8563, 8573, 8581, 8597, 8599, 8609, 8623, 8627, 8629, 8641, 8647, 8663, 8669, 8677, 8681, 8689, 8693, 8699, 8707, 8713, 8719, 8731, 8737, 8741, 8747, 8753, 8761, 8779, 8783, 8803, 8807, 8819, 8821, 8831, 8837, 8839, 8849, 8861, 8863, 8867, 8887, 8893, 8923, 8929, 8933, 8941, 8951, 8963, 8969, 8971, 8999, 9001, 9007, 9011, 9013, 9029, 9041, 9043, 9049, 9059, 9067, 9091, 9103, 9109, 9127, 9133, 9137, 9151, 9157, 9161, 9173, 9181, 9187, 9199, 9203, 9209, 9221, 9227, 9239, 9241, 9257, 9277, 9281, 9283, 9293, 9311, 9319, 9323, 9337, 9341, 9343, 9349, 9371, 9377, 9391, 9397, 9403, 9413, 9419, 9421, 9431, 9433, 9437, 9439, 9461, 9463, 9467, 9473, 9479, 9491, 9497, 9511, 9521, 9533, 9539, 9547, 9551, 9587, 9601, 9613, 9619, 9623, 9629, 9631, 9643, 9649, 9661, 9677, 9679, 9689, 9697, 9719, 9721, 9733, 9739, 9743, 9749, 9767, 9769, 9781, 9787, 9791, 9803, 9811, 9817, 9829, 9833, 9839, 9851, 9857, 9859, 9871, 9883, 9887, 9901, 9907, 9923, 9929, 9931, 9941, 9949, 9967, 9973]
                if n in smallprimes:
                    return True
                for sp in smallprimes:
                    if n%sp==0:
                        return False
                for i in range(smallprimes[-1], _math.ceil(_math.sqrt(n))+1, 2):
                    if n%i==0:
                        return False
                return True
            case 5:
                if len(cls.primes)<10000:
                    primes = [2]
                    for i in range(3,1_000_000,2):
                        for p in primes:
                            if i%p==0:
                                break
                            if p>_math.ceil(_math.sqrt(i))+1:
                                primes.append(i)
                                break
                        else:
                            primes.append(i)
                    cls.primes = primes
                if n in cls.primes:
                    return True
                for sp in cls.primes:
                    if n%sp==0:
                        return False
                for i in range(cls.primes[-1], _math.ceil(_math.sqrt(n))+1, 2):
                    if n%i==0:
                        return False
                return True
            case _:
                if n==2:
                    return True
                if n&1==0: # n の最下位ビットが0＝偶数
                    return False
                def mp(base, power, mod):
                    result = 1
                    while power>0:
                        if power&1 == 1:
                            result = (result * base) % mod
                        base = (base * base) % mod
                        power >>= 1
                    return result
                d = n-1
                while d&1 == 0:
                    d >>= 1
                for _ in range(20):
                    a = _random.randint(1,n-1)
                    t = d
                    y = mp(a,t,n)
                    while t != n-1 and y != 1 and y != n-1:
                        y = (y * y) % n
                        t <<= 1
                    if y != n-1 and t&1 == 0:
                        return False
                return True    
    @staticmethod
    def generateprimesto(n:int):
        "generate prime numbers up to `n`"
        if n<=1:
            raise ValueError("`n` must be greater than 1")
        primes = [2]
        for i in range(3,n,2):
            for p in primes:
                if i%p==0:
                    break
                if p>_math.ceil(_math.sqrt(n))+1:
                    primes.append(i)
                    break
            else:
                primes.append(i)
        return primes
    @staticmethod
    def generateprimesby(n:int):
        "generate prime numbers `n`times"
        if n<=0:
            raise ValueError("`n` must be greater than 0")
        primes = [2]
        i = 3
        while len(primes)<n:
            for p in primes:
                if i%p==0:
                    break
                if p>_math.ceil(_math.sqrt(i))+1:
                    primes.append(i)
                    break
            else:
                primes.append(i)
            i+=2
        return primes
    
    @classmethod
    def pi(cls, selector:piCalcurator=piCalcurator.RAMANUJAN,N:int=10,*,ROOTS:int=10,LIMITS:int=0):
        if N<=0:
            raise ValueError("`N` must be greater than 0")
        pi = _Fraction(0)
        match selector:
            case cls.piCalcurator.RAMANUJAN:
                sum = _Fraction(1123,882)
                for i in range(1,N):
                    sum += _Fraction((((-1)**i) * _math.factorial(4*i) * (1123+21460*i)) , ((882**(2*i+1)) * (((4**i) * _math.factorial(i))**4)))
                    if LIMITS!=0:
                        sum = sum.limit_denominator(LIMITS)
                pi = _Fraction(4*sum.denominator,sum.numerator)
            case cls.piCalcurator.MONTECARLO:
                x = [_random.random() for _ in range(N)]
                y = [_random.random() for _ in range(N)]
                counter = 0
                for i in range(N):
                    if _math.dist((0,0),(x[i],y[i]))<=1:
                        counter += 1
                pi = _Fraction(4 * counter, N)
            case cls.piCalcurator.LEIBNIZ:
                pi = _Fraction(0)
                for i in range(N):
                    pi += _Fraction(2,16*(i+1)*i+3)
                    if LIMITS!=0:
                        pi = pi.limit_denominator(LIMITS)
                pi = pi*4
            case cls.piCalcurator.TRAPEZOIDALRULE:
                h = _Fraction(1,N)
                pi = _Fraction(0)
                for i in range(N):
                    pi += (cls.f_root(1-(i*h)**2,ROOTS)+cls.f_root(1-(i*h+h)**2,ROOTS))*h/2
                    if LIMITS!=0:
                        pi = pi.limit_denominator(LIMITS)
                pi = pi*4
            case cls.piCalcurator.WALLISPRODUCT:
                pi = _Fraction(2*2,1*3)
                for i in range(2,N+1):
                    pi *= _Fraction(4*i*i,4*i*i-1)
                    if LIMITS!=0:
                        pi = pi.limit_denominator(LIMITS)
                pi = pi*2
            case cls.piCalcurator.RAMANUJAN1914:
                sum = _Fraction(1103,1)
                for i in range(1,N):
                    sum += _Fraction(_math.factorial(4*i), (4**i*_math.factorial(i))**4)*_Fraction(1103+26390*i, 99**(4*i))
                    if LIMITS!=0:
                        sum = sum.limit_denominator(LIMITS)
                pi = _Fraction(2*cls.f_root(_Fraction(2),ROOTS),9801)*sum
                pi = 1/pi
            case cls.piCalcurator.CHUDNOVSKY:
                A:int = 13591409
                B:int = 545140134
                C:int = 640320**3
                sum = _Fraction(0)
                for i in range(N):
                    sum += _Fraction(((-1)**i)*_math.factorial(6*i), _math.factorial(3*i)*((_math.factorial(i))**3))*_Fraction(A+B*i, C**i)
                    if LIMITS!=0:
                        sum = sum.limit_denominator(LIMITS)
                pi = (12/cls.f_root(_Fraction(C),ROOTS))*sum
                pi = 1/pi
            case cls.piCalcurator.BORWEIN:
                R61:_Fraction = cls.f_root(61,ROOTS)
                A:_Fraction = 1657145277365 + (212175710912*R61)
                B:_Fraction = 107578229802750 + (13773980892672*R61)
                C:_Fraction = (5280 * (236674+(30303*R61)))**3
                sum = _Fraction(0)
                for i in range(N):
                    sum += _Fraction(((-1)**i)*_math.factorial(6*i), _math.factorial(3*i)*((_math.factorial(i))**3))*_Fraction(A+B*i, C**i)
                    if LIMITS!=0:
                        sum = sum.limit_denominator(LIMITS)
                pi = (12/cls.f_root(C.limit_denominator(LIMITS),ROOTS))*sum
                pi = 1/pi
            case cls.piCalcurator.GAUSSLEGENDRE:
                a = _Fraction(1)
                b = 1/cls.f_root(_Fraction(2),ROOTS)
                t = _Fraction(1,4)
                p = _Fraction(1)
                for i in range(N):
                    a,b,t,p = (a+b)/2, cls.f_root(a*b,ROOTS), t-p*(a-((a+b)/2))**2, 2*p
                    if LIMITS!=0:
                        a,b,t,p = a.limit_denominator(LIMITS), b.limit_denominator(LIMITS), t.limit_denominator(LIMITS), p.limit_denominator(LIMITS)
                pi = ((a + b) ** 2)/(4*t)
                pi = pi
            case cls.piCalcurator.EULER:
                sum = _Fraction(1)
                for i in range(2,N+1):
                    sum += _Fraction(1,i*i)
                    if LIMITS!=0:
                        sum = sum.limit_denominator(LIMITS)
                pi = sum*6
                pi = cls.f_root(pi,ROOTS)
            case cls.piCalcurator.BAILEYBORWEINPLOUFFE:
                # TODO: more efficient programming
                pi = _Fraction(0)
                for i in range(N):
                    pi += _Fraction(1,16**i)*(_Fraction(4,8*i+1)-_Fraction(2,8*i+4)-_Fraction(1,8*i+5)-_Fraction(1,8*i+6))
                    if LIMITS!=0:
                        pi = pi.limit_denominator(LIMITS)
                pi = pi
            case cls.piCalcurator.BELLARD:
                # TODO: more efficient programming
                pi = _Fraction(0)
                for i in range(N):
                    pi += _Fraction((-1)**i,2**(10*i))*(-_Fraction(2**5,4*i+1)-_Fraction(1,4*i+3)+_Fraction(2**8,10*i+1)-_Fraction(2**6,10*i+3)-_Fraction(2**2,10*i+5)-_Fraction(2**2,10*i+7)+_Fraction(1,10*i+9))
                    if LIMITS!=0:
                        pi = pi.limit_denominator(LIMITS)
                pi = pi*_Fraction(1,2**6)
            case cls.piCalcurator.高野喜久雄:
                at49 = cls.arctan(_Fraction(1,49),N)
                at57 = cls.arctan(_Fraction(1,57),N)
                at239 = cls.arctan(_Fraction(1,239),N)
                at110443 = cls.arctan(_Fraction(1,110443),N)
                pi = 4*(12*at49 + 32*at57 - 5*at239 + 12*at110443)
            case _:
                pi = _Fraction(_math.pi)
        if LIMITS==0:
            return pi
        return pi.limit_denominator(LIMITS)
    
    @staticmethod
    def _BSm(a:_Callable[[_Fraction,int],_Fraction],b:_Callable[[_Fraction,int],_Fraction],p:_Callable[[_Fraction,int],_Fraction],q:_Callable[[_Fraction,int],_Fraction],x:_Fraction,n:int):
        s = _Fraction(0)
        for i in range(n):
            ans = a(x,i)/b(x,i)
            ansp = p(x,0)
            ansq = q(x,0)
            for j in range(1,i+1): # for [0,n] range function needs to be +1
                ansp *= p(x,j)
                ansq *= q(x,j)
            ans *= ansp/ansq
            s += ans
        return _deepcopy(_Fraction(s))
    
    @staticmethod
    def e(N:int=100):
        return sum([_Fraction(1,_math.factorial(i)) for i in range(N)])
    @classmethod
    def exp(cls, x:_Fraction,N:int):
        def a(x:_Fraction, n:int) -> _Fraction: return _Fraction(1)
        def b(x:_Fraction, n:int) -> _Fraction: return _Fraction(1)
        def p(x:_Fraction, n:int) -> _Fraction: return _Fraction(1) if n==0 else _Fraction(x.numerator)
        def q(x:_Fraction, n:int) -> _Fraction: return _Fraction(1) if n==0 else _Fraction(n * x.denominator)
        return cls._BSm(a,b,p,q,x,N)

    @classmethod
    def lnp1(cls, x:_Fraction,N:int):
        if x<-1:
            raise ValueError("`x` must be greater than or equal to -1")
        if x>1:
            raise ValueError("`x` must be less than or equal to 1") # Cannot be calculated for large values
        if not isinstance(x, _Fraction):
            raise TypeError("`x` must be Fraction class. If you want to use other type variable, use `ln()`")
        def a(x:_Fraction, n:int) -> _Fraction: return _Fraction(1)
        def b(x:_Fraction, n:int) -> _Fraction: return _Fraction(n+1)
        def p(x:_Fraction, n:int) -> _Fraction: return _Fraction(x.numerator) if n==0 else _Fraction(-1 * x.numerator)
        def q(x:_Fraction, n:int) -> _Fraction: return _Fraction(x.denominator)
        return cls._BSm(a,b,p,q,x,N)
    def ln(self, x:_SupportsFloat,N:int):
        if x<=0 or 2<=x:
            raise ValueError("xの定義域は(0,2)です。")
        return self.lnp1(_Fraction(x)-_Fraction(1, 1),N)
    
    def log(self, x:_Fraction,N:int, LIMITS:int=0):
        # TODO: function lnp1 can be used between -1<x<1 make this 0<x<inf
        if not isinstance(x, _Fraction):
            raise TypeError("`x` must be Fraction class.")
        # 場合分けを行う
        # [1] log_eは定義域が(0,inf)なので、その外側はエラー
        if x<=0:
            raise ValueError("xの定義域は(0,inf)です。")
        # [2] (0,2)の場合はx-1をしてlnp1に渡す
        if 0<x and x<2:
            return self.lnp1(x-1, N)
        # [3] [2,?]の場合はln(x)=-ln(1/x)から求める。ln(x)はx=t+1としてt=x-1からln(1+t)=ln(1+x-1)よりlnp1にx-1を渡す
        #     つまり、2<=xに対してp,tが存在し、ln(x)=-ln(1/x)=-ln(p)=-ln(1+p-1)=-ln(1+t), p=1/x|t=p-1 => t=1/x-1
        #     したがって、ln(x)=-ln(1+ (1/x-1) )
        #     ここで、lnp1の精度を鑑みると、実際にはx=10^5程度までしか適切に演算できない
        #     よって、10<<xにおいては、log_2について考え、log_e(2)log_2(x)よりln(x)を求めるのが適する。
        if 2<=x<self.E**10:
            return -self.lnp1((1/x)-1, N)
        if self.E**10<=x:
            log2_x = _Fraction(x.numerator.bit_length()-x.denominator.bit_length())
            for _ in range(N):
                #log2_x = log2_x - ((2**log2_x-x) / 2**log2_x)
                # ERROR!!! 2^log2_x = x, log2_x=log2_x-((x-x)/x)=log2_x-0 <- ???
                p2x = self.powBinFract(log2_x,N,LIMITS) if LIMITS>0 else self.powBinFract(log2_x,N)
                log2_x = log2_x - ((p2x-x)/(p2x))
                if LIMITS>0:
                    log2_x = log2_x.limit_denominator(LIMITS)
                print(p2x,"\n",log2_x)
            return -self.lnp1(_Fraction(-1,2), N)*log2_x
        return None

    @classmethod
    def sin(cls, x:_Fraction,N:int):
        def a(x:_Fraction, n:int) -> _Fraction: return _Fraction(1)
        def b(x:_Fraction, n:int) -> _Fraction: return _Fraction(1)
        def p(x:_Fraction, n:int) -> _Fraction: return _Fraction(x.numerator) if n==0 else _Fraction(-x.numerator*x.numerator)
        def q(x:_Fraction, n:int) -> _Fraction: return _Fraction(x.denominator) if n==0 else _Fraction(2*n*(2*n+1) * x.denominator*x.denominator)
        return cls._BSm(a,b,p,q,x,N)
    @classmethod
    def cos(cls, x:_Fraction,N:int):
        def a(x:_Fraction, n:int) -> _Fraction: return _Fraction(1)
        def b(x:_Fraction, n:int) -> _Fraction: return _Fraction(1)
        def p(x:_Fraction, n:int) -> _Fraction: return _Fraction(1) if n==0 else _Fraction(-x.numerator*x.numerator)
        def q(x:_Fraction, n:int) -> _Fraction: return _Fraction(1) if n==0 else _Fraction(2*n*(2*n-1) * x.denominator*x.denominator)
        return cls._BSm(a,b,p,q,x,N)
    @classmethod
    def arctan(cls, x:_Fraction,N:int):
        def a(x:_Fraction, n:int) -> _Fraction: return _Fraction(1)
        def b(x:_Fraction, n:int) -> _Fraction: return _Fraction(2*n+1)
        def p(x:_Fraction, n:int) -> _Fraction: return x if n==0 else -x*x
        def q(x:_Fraction, n:int) -> _Fraction: return _Fraction(1)
        return cls._BSm(a,b,p,q,x,N)

    @staticmethod
    def epsilon(t:int|float|_Decimal|_Fraction|_SupportsFloat, c:int|float|_Decimal|_Fraction|_SupportsFloat):
        "`t` is test value, `c` is calcurated value"
        if type(t)!=type(c):
            raise TypeError(f"Object type is not same, t:{type(t)} and c:{type(c)} was given")
        match t:
            case int():
                return (int(t) - int(c))/int(c)
            case float():
                return (float(t) - float(c))/float(c)
            case _Decimal():
                return (_Decimal(t) - _Decimal(c))/_Decimal(c)
            case _Fraction():
                return (_Fraction(t) - _Fraction(c))/_Fraction(c)
            case _:
                return (t-c)/c
        return (t-c)/c
    
    @staticmethod
    def epsilon_selector(t:str, c:str, tp:str):
        match str(tp).lower():
            case "int"|"integer":
                return (int(t) - int(c))/int(c)
            case "float"|"double":
                return (float(t) - float(c))/float(c)
            case "decimal"|"dec"|"deci"|"d":
                return (_Decimal(t) - _Decimal(c))/_Decimal(c)
            case "fraction"|"frac"|"fract"|"f":
                return (_Fraction(t) - _Fraction(c))/_Fraction(c)
            case _:
                raise ValueError("idk y u raise Exception")

"""logarithm

math.log(a) -> log_e(a)

math.log(a, n) -> log_n(a)

"""

def digits(n:_Any) -> int:
    "Return: digits of `n`"
    return int(_math.log10(n))+1

def intstrlen(n:int):
    "Return: length of `n`"
    return len(str(abs(n)))

def easyintlog2(n:int) -> int:
    "Not truly log2ed, but super low calc"
    return n.bit_length()-1

def intdigits(n:int) -> int:
    "Search the digits of `n` with loop processing"
    if _sys.float_info.max<n:
        dig = 1
        lbn = easyintlog2(n)
        while(dig*_math.log2(10)<lbn):
            dig += 1
        return dig
    else:
        dig = 1
        while(10**dig<=n):
            dig += 1
        return dig-1

def intdivision(n:int,m:int) -> int:
    "divide calculation only use int"
    return int(n // m + (0 if n%m*10/m<5 else 1))

def intlog10(n:int) -> int:
    "Not truly log10ed, but only use int for calculation"
    idig = intdigits(n)
    if(idig-_sys.float_info.max_10_exp+digits(_math.log2(10))<0):
        return intdivision(easyintlog2(n)*(10**idig),int(_math.log2(10)*(10**idig)))
    return intdivision(easyintlog2(n)*(10**idig),int(_math.log2(10)*10**(_sys.float_info.max_10_exp-digits(_math.log2(10))))*int(10**(idig-_sys.float_info.max_10_exp+digits(_math.log2(10)))))

def myaboutlog10accuracy(n:float):
    "for `intlog10()` function to check accuracy rate"
    if n==1:
        return 100
    return (intlog10(int(n))-_math.log10(n))/_math.log10(n)*100

def brlog10(n):
    "log10 selector for big range of n"
    if(type(n)==float):
        return _math.log10(n)
    elif(type(n)==int):
        if(intlog10(n)<(10**_sys.float_info.max_10_exp)):
            return _math.log10(n)
        else:
            return intlog10(int(n))
    else:
        return None
    
def compound_number(frac:_Fraction) -> tuple[int,_Fraction]:
    "Returns: (base, frac) from normal `Fraction` to compounded."
    if frac==_Fraction(1):
        return 1,_Fraction(0)
    if frac.numerator<frac.denominator:
        return 0,frac
    # n>d(n/d)
    base = _math.floor(frac)
    return base,frac-base
def infinite_precision(frac:_Fraction, precision:int=1000) -> tuple[int,int]:
    "Returns: (mantissa, exponent) from fraction to infinite precision `int`class"
    sign = -1 if frac<0 else 1
    frac = abs(frac)
    mantissa, cp_frac = compound_number(frac)
    expo = 0
    while cp_frac!=_Fraction(0):
        mantissa *= 10
        cp_frac *= 10
        b, cp_frac = compound_number(cp_frac)
        mantissa += b
        expo += 1
        if 0<precision and precision<=expo:
            break
    return (sign*mantissa,expo)
def infinite_precision_error(frac:_Fraction, precision:int=1000) -> _Fraction:
    "Return: Fraction calculate epsilon of `infinite_precision()`"
    frac = abs(frac)
    _, cp_frac = compound_number(frac)
    expo = 0
    while cp_frac!=_Fraction(0):
        cp_frac *= 10
        _, cp_frac = compound_number(cp_frac)
        expo += 1
        if 0<precision and precision<=expo:
            break
    return cp_frac
def infinite_format_stringer(mantissa:int, expo:int):
    # mantissa*10^-expo
    mstring = str(mantissa)
    mdigits = len(mstring)
    string = ""
    if expo==0:
        return mstring
    if mdigits>expo:
        string = mstring[:mdigits-expo] + "." + mstring[mdigits-expo:]
    elif mdigits==expo:
        string = "0." + mstring
    else:
        string = "0." + "0"*(expo-mdigits) + mstring
    return string
def Fraction_to_Decimal(frac:_Fraction, precision:int=1000):
    return _Decimal(infinite_format_stringer(*infinite_precision(frac=frac, precision=precision)))

def float_error(*,zeropoint:int) -> float:
    "Input:0.[zeropoint:int] Return: error of floating point number"
    fi = infinite_precision(_Fraction(float(f"0.{zeropoint}")))
    ex2 = 0
    ex5 = 0
    for i in range(int(_math.log(zeropoint, 2))+1):
        if zeropoint%2**i==0:
            ex2 = i
    for i in range(int(_math.log(zeropoint, 5))+1):
        if zeropoint%5**i==0:
            ex5 = i
    truezeropoint = int(zeropoint/10**min(ex2,ex5))
    return (fi[0] - truezeropoint * 10**(fi[1]-int(_math.log10(truezeropoint)+1))) / 10**fi[1]

def to_ieee754(x:float): # 'bias': 1023, 'exp_bits': 11, 'mantissa_bits': 52, 8bytes = 64bits
    "From `float` to representation of IEEE754"
    if x==0:
        if str(x)[0]=="0":
            return "0"*64
        else:
            return "1"+"0"*63
    sign = 0 if x>=0 else 1
    x = abs(x)
    itx = int(x)
    flx = x-itx
    bitx = bin(itx)[2:]
    i = 1
    bflx = ""
    while flx!=0.0:
        if not 2**-i<=flx:
            bflx += "0"
            i+=1
        else:
            bflx += "1"
            flx -= 2**-i
            i+=1
    bnx = f"{bitx}.{bflx}"
    pp = bnx.find('.')
    fo = bnx.find('1')
    exponent = pp-fo-1
    if fo>pp:
        exponent = pp-fo
    exponent += 1023 # bias
    mantissa = (bitx+bflx)[((bitx+bflx).find('1'))+1:]
    ieee754 = f"{sign}{("0"*11+bin(exponent)[2:])[-11:]}{(mantissa+"0"*52)[:52]}"
    return ieee754
def from_ieee754(s:str):
    "From representation of IEEE754 to `float`"
    if len(s)!=64:
        raise ValueError("Not Correct Value")
    if s == "0"*64:
        return 0.0
    elif s == "1"+"0"*63:
        return -0.0
    sign, exponent, mantissa = int(s[0]), int(s[1:11+1],2), s[11+1:]
    fl = 1.0
    for i in range(len(mantissa)):
        fl += int(mantissa[i])*2**-(i+1)
    fl *= 2**(exponent-1023)
    fl *= (-1)**sign
    return fl
def to_ieee754_bytes(x:float):
    "`to_ieee` output bytes type"
    return int(to_ieee754(x),2).to_bytes(8)
def from_ieee754_bytes(x:bytes):
    "`from_ieee` input bytes type"
    return from_ieee754(bin(int.from_bytes(x))[2:])

def get_dhmsu(sec:float):
    td = _datetime.timedelta(seconds=sec)
    m,s = divmod(td.seconds, 60)
    h,m = divmod(m, 60)
    return td.days, h, m, s, td.microseconds

def y2d(y:int) -> int:
    "from year to days"
    return 365*y+int(y/4)-int(y/100)+int(y/400)

def timestamp2ISO8601(t:float):
    "From timestamp to ISO8601 format of date"
    year = int(t//(60*60*24*365.25))+1970
    year = year if y2d(year-1)-y2d(1969)<=t/(60*60*24)<y2d(year)-y2d(1969) else (year-1 if t/(60*60*24)<=y2d(year)-y2d(1969) else year+1)
    days = int(t)//(60*60*24)-(y2d(year-1)-y2d(1970-1))+1
    # print(days)
    endofmonth = [31,29 if year%4==0 and ( year%100!=0 or year%400==0 ) else 28,31,30,31,30,31,31,30,31,30,31]
    month = sum([1 for i in range(1,12+1) if sum(endofmonth[:i])<days])+1
    endofbeforelast = sum(endofmonth[:month-1])
    # print(days,endofbeforelast)
    day = int(days-endofbeforelast)
    total_seconds = t%int(60*60*24)
    hour = int(total_seconds//(60*60))
    minute = int(total_seconds%(60*60)//60)
    sec = int(total_seconds%60)
    nosec = int(t*1000000)%1000000
    return f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{sec:02d}.{nosec:06d}"

def clearconsole():
    "PRINT 10000 lanes of `\\n`"
    print("\n"*10000, end="")
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

def xorhash(hash1:str,hash2:str):
    "from 2hashes to xored hash"
    return hex(int(hash1,base=16)^int(hash2,base=16))[2:]

def UTF8num(string:str) -> int:
    "From utf_8 to num of character code"
    return int.from_bytes(string.encode("utf-8"))
def numUTF8(num:int) -> str:
    "From num of character code to utf_8"
    return get_bytes(num).decode("utf-8")
def get_bytes(num:int, byteorder: _Literal['little', 'big'] = "big",*, signed: bool = False) -> bytes:
    "from any `int` to `bytes`"
    return num.to_bytes((num.bit_length()+7)//8, byteorder=byteorder, signed=signed)

def slit(string:str,wide:int) -> list[str]:
    "From long `string` to list with `string` divided per `wide`"
    return [string[i:i+wide] for i in range(0,len(string),wide)]

def macaddress():
    "Return this machine's Mac Address"
    return ":".join(slit(hex(_getnode())[2:],2))
def ipaddress():
    "Return this machine's IP Address"
    return _gethostbyname(_gethostname())

def my_function_call_function(input:_Any,func:_Callable):
    "this function calls `func`function and inputs `input` to it and returns the returned data"
    return func(input)

def mutablecopy(mutable,loop:int):
    """copy table using deepcopy

    Example:
    >>> nonmuted = mutablecopy({"how":0},2)
    >>> muted = [{"how":0}]*2
    >>> nonmuted[1]["how"] = 2
    >>> muted[1]["how"] = 2
    >>> nonmuted
    [{'how': 0}, {'how': 2}]
    >>> muted
    [{'how': 2}, {'how': 2}]
    """
    return [_deepcopy(mutable) for _ in range(loop)]

def get_dir_size(path='.',recursion=True,follow_symlinks=True):
    "get directory size"
    total = 0
    with _os.scandir(path=path) as deit: # DirEntry iterator
        for entry in deit:
            if entry.is_file(follow_symlinks=follow_symlinks):
                total += entry.stat().st_size
            elif recursion and entry.is_dir(follow_symlinks=follow_symlinks):
                total += get_dir_size(entry.path)
    return total

def get_external_size(path='.'):
    "get external things size"
    if _os.path.isfile(path):
        return _os.path.getsize(path)
    elif _os.path.isdir(path):
        return get_dir_size(path)

def get_dir_size_old(path='.'):
    "if python version is older than 3.11(?), you can only use this function"
    total = 0
    for p in _os.listdir(path=path):
        full_path = _os.path.join(path, p)
        if _os.path.isfile(full_path):
            total += _os.path.getsize(full_path)
        elif _os.path.isdir(full_path):
            total += get_dir_size_old(full_path)
    return total

def compute_object_size(o, handlers={}):
    "computes `o`object size"
    dict_handler = lambda d: _chain.from_iterable(d.items())
    all_handlers = {tuple: iter,
                    list: iter,
                    _deque: iter,
                    dict: dict_handler,
                    set: iter,
                    frozenset: iter,
                   }
    all_handlers.update(handlers)     # user handlers take precedence
    seen = set()                      # track which object id's have already been seen
    default_size = _sys.getsizeof(0)       # estimate sizeof object without __sizeof__

    def sizeof(o):
        if id(o) in seen:       # do not double count the same object
            return 0
        seen.add(id(o))
        s = _sys.getsizeof(o, default_size)

        for typ, handler in all_handlers.items():
            if isinstance(o, typ):
                s += sum(map(sizeof, handler(o)))
                break
        return s

    return sizeof(o)

def unitparser(unitstr:str):
    unitstr = unitstr.replace(" ", "")
    unitstr = unitstr.replace("_", "")
    unitstr = unitstr.replace(",", "")

    NUMB = [str(i) for i in range(10)]
    SIUT = ["p", "n", "μ", "u", "m", "c", "d", "da", "h", "k", "K", "M", "G", "T", "P"] # da = deka <- never hits
    rSIU = [1e-12, 1e-9, 1e-6, 1e-6, 1e-3, 1e-2, 1e-1, 1e1, 1e2, 1e3, 1e3, 1e6, 1e9, 1e12, 1e15]

    fixedint = ""
    fixedfloat = ""
    separatorflag = False
    siunitbase = "0"

    for i in range(len(unitstr)):
        if unitstr[i] in NUMB:
            if separatorflag:
                fixedfloat += unitstr[i]
            else:
                fixedint += unitstr[i]
        elif unitstr[i] == ".":
            separatorflag = True
        elif unitstr[i] in SIUT:
            tmp = rSIU[SIUT.index(unitstr[i])]
            if tmp < 1:
                siunitbase = f"{{:.{f"{tmp:g}"[3:]}f}}".format(tmp)
            else:
                siunitbase = str(tmp)
            unitindex = i+1
            break
        else:
            unitindex = i

    unit = unitstr[unitindex:]

    return fixedint, fixedfloat, siunitbase, unit

def BytesToSIUnit(size:int, isdata:bool=True, dataformat:bool=True) -> str:
    "from `size` to size with si unit"
    base = 1024 if isdata else 1000
    logged = _math.log(size, base)
    kmgt = int(logged)
    SIunit = ""
    if dataformat:
        match kmgt:
            case 0:
                SIunit = "  B"
            case 1:
                SIunit = "kiB" # kibibyte キビバイト
            case 2:
                SIunit = "MiB" # mebibyte メビバイト
            case 3:
                SIunit = "GiB" # gibibyte ギビバイト
            case 4:
                SIunit = "TiB" # tebibyte テビバイト
            case 5:
                SIunit = "PiB" # pebibyte ペビバイト
            case 6:
                SIunit = "EiB" # exbibyte エクスビバイト
            case 7:
                SIunit = "ZiB" # zebibyte ゼビバイト
            case 8:
                SIunit = "YiB" # yobibyte ヨビバイト
            case 9:
                SIunit = "RiB" # robibyte ロビバイト
            case 10:
                SIunit = "QiB" # quebibyte クエビバイト
            case _:
                SIunit = "Bytes"
    else:
        match kmgt:
            case 0:
                SIunit = " B"
            case 1:
                SIunit = "kB" # kilobyte キロバイト
            case 2:
                SIunit = "MB" # megabyte メガバイト
            case 3:
                SIunit = "GB" # gigabyte ギガバイト
            case 4:
                SIunit = "TB" # terabyte テラバイト
            case 5:
                SIunit = "PB" # petabyte ペタバイト
            case 6:
                SIunit = "EB" # exabyte エクサバイト
            case 7:
                SIunit = "ZB" # zettabyte ゼタバイト
            case 8:
                SIunit = "YB" # yottabyte ヨタバイト
            case 9:
                SIunit = "RB" # ronnabyte ロナバイト
            case 10:
                SIunit = "QB" # quettabyte クエタバイト
            case _:
                SIunit = "Bytes"
    return f"{size/(base**kmgt):.4f} {SIunit}"

def NoOverride(filepath:str) -> str:
    "Do Not Override with using this function"
    directory, filename = _os.path.split(filepath)
    if not _os.path.isdir(directory):
        raise FileNotFoundError(f"No such directory: '{directory}'")
    if filename in _os.listdir(directory):
        idx = 0
        fn = f"{_os.path.splitext(filename)[0]}_{idx}{_os.path.splitext(filename)[1]}"
        while fn in _os.listdir(directory):
            idx += 1
            fn = f"{_os.path.splitext(filename)[0]}_{idx}{_os.path.splitext(filename)[1]}"
        return _os.path.join(directory, fn)
    else:
        return filepath
    return ""

def leftshift(s:str):
    return _deepcopy(s[1:]+s[0])
def Burrows_Wheeler_Algorithm_encode(string:str):
    shift_list = []
    for _ in range(len(string)):
        shift_list.append(string)
        string = leftshift(string)
    sorted_shift_list = sorted(shift_list)
    return "".join([s[-1] for s in sorted_shift_list]),sorted_shift_list.index(string)
def Burrows_Wheeler_Algorithm_decode(string:str,index:int):
    sorted_shift_list = [""]*len(string)
    for _ in range(len(string)):
        for i in range(len(sorted_shift_list)):
            sorted_shift_list[i] = string[i]+sorted_shift_list[i]
        sorted_shift_list = sorted(sorted_shift_list)
    return sorted_shift_list[index]

ACCESSIBLES = list(sorted([k for k in list(locals().keys()) if k[0]!='_']))
"""このモジュールで使えるアクセッサ一覧です。

Example:
>>> for acc in anyfunction.ACCESSIBLES:
>>>     print("\\n\\n\\n")
>>>     print(acc)
>>>     eval(f"print(af.{acc}.__doc__)")
"""

# 注意！ 以下違反コード

def mydeprecated(message:_LiteralString):
    def _mydepre(func:_Callable):
        def wrapper(*args, **kwargs):
            _warn(message,DeprecationWarning)
            func(*args, **kwargs)
        return wrapper
    return _mydepre

if int(_python_version_tuple()[0])>=3 and int(_python_version_tuple()[1])>=13:
    from warnings import deprecated
    @deprecated("Too small to stop code.")
    def qt():
        quit()
else:
    @mydeprecated("Too small to stop code.")
    def qt():
        quit()

if __name__ == "__main__":
    import code
    print("Hello, World!")
    class quitting:
        def __init__(self) -> None:
            pass
        def __repr__(self) -> str:
            qt()
            return ""
        def __str__(self) -> str:
            qt()
            return ""
    q = quitting()
    print(timestamp2ISO8601(_time.time()))
    code.InteractiveConsole(locals=locals()).interact()
