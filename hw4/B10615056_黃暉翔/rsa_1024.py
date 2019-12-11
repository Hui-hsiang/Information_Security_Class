#%%
import numpy as np
import pandas as py
import random
import sys
import math

#%%
def hcfnaive(a,b): 
    if(b==0): 
        return a 
    else: 
        return hcfnaive(b,a%b) 
#%%
def xgcd(a, b):
    """return (g, x, y) such that a*x + b*y = g = gcd(a, b)"""
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        q, b, a = b // a, a, b % a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return b, x0, y0
#%%
def modinv(a, b):
    """return x such that (x * a) % b == 1"""
    g, x, _ = xgcd(a, b)

    if g == 1:
        return x % b
    else:
        raise Exception('modular inverse does not exist')
        
#%%
def exp_mod( a, b, n):
    """return (a ** b )%n"""
    r = int(1)
    while(b):
        if(b&1):
            r=(r*a)%n
        a=(a*a)%n
        b>>=1       # b = b>>1
    
    return r

#%%
def gen_prime():
    prime = ''
    for i in range(1024):
        if i == 1023 or i == 0:
            prime += '1'
        else:
            prime += random.choice(['0','1'])


    while isprime(prime) == False:
        prime = ''
        for i in range(1024):
            if i == 1023 or i == 0:
                prime += '1'
            else:
                prime += random.choice(['0','1'])
    return int(prime,2)
# %%
def isprime(n):
    n = int(n,2)
    if (n == 2 ):
        return True
    if (n < 2): 
        return False

    a = random.randint(1,n) % (n-2) + 2
 
    u = n-1 
    t = 0
    while (u % 2 == 0):
        u >>= 1
        t+=1
 
    x = exp_mod(a, u, n)  # x = a ^ u % n
    if (x == 1 or x == n-1): 
        return True
 
    for i in range(t-1):
    
        x = exp_mod(x, 2, n);   # x = x * x % n;
        if (x == 1): 
            return False
        if (x == n-1): 
            return True
    
    return False


# %%
def key_generator():
    p = gen_prime()
    q = gen_prime()
    n = p * q
    # print('p = ',p)
    # print('q = ',q)
    # print('n = ',n)
    phi_n = (p - 1) * (q - 1)
    pe = [e for e in range(10000) if hcfnaive(e,phi_n) == 1]
    e = random.choice(pe)
    while (1):
        try:
            d = modinv(e, phi_n)
            break
        except:
            p = gen_prime()
            q = gen_prime()
            n = p * q
            phi_n = (p - 1) * (q - 1)
            continue

    # print('e = ',e)
    # print('d = ',d)
    return p,q,n,e,d

# %%
def encypher(plaintext,n,e):
    ciphertext = []
    for char in plaintext:
        c = ord(char)
        ciphertext.append(exp_mod(c,e,n))
    return ciphertext
# %%
def decypher(ciphertext,n,d):
    pt = []
    for char in ciphertext:
        pt.append(exp_mod(char,d,n))
    plaintext = ""
    for i in pt:
        plaintext += chr(i)

    return plaintext

# %%
if __name__ == "__main__":
    argv = sys.argv
    plaintext = argv[1]

    
    p,q,n,e,d = key_generator()
    print('p = ',p)
    print('q = ',q)
    print('n = ',n)
    print('e = ',e)
    print('d = ',d)
    ciphertext = encypher(plaintext,n,e)
    print ('ciphertext :',ciphertext)
    plaintext = decypher(ciphertext,n,d)
    print ('plaintext :',plaintext)



# %%
