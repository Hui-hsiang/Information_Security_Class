#%%
import numpy as nu
import pandas as py
import random
import sys




#%%
def key_generator(maxPrime):
    primes = [i for i in range(0,maxPrime) if isPrime(i)]
    p = random.choice(primes)
    primes.remove(p)
    q = random.choice(primes)
    n = p*q
    phi_N = (p-1)*(q-1)
    pe = [e for e in range(phi_N - 1) if hcfnaive(e,phi_N) == 1]
    e = random.choice(pe)
    for d in range(phi_N):
        if (d * e) % phi_N == 1:
            break

    print ('p = ',p,'q = ',q,'n = ',n,'e = ',e,'d = ',d)
#%%
def encypher(plaintext,n,e):
    ciphertext = ""
    for char in plaintext:
        c = ord(char)
        ciphertext += (chr(pow(c,e,n)))
    
    print (ciphertext)
#encypher('hello',674, 257)
#%%
def decypher(ciphertext,n,d):
    plaintext = ""
    for char in ciphertext:
        c = ord(char)
        plaintext += (chr(pow(c,d,n)))
    print (plaintext)
#decypher('Ʌppo',674, 17)

#%%
def isPrime(n):
    if n == 0 or n == 1:
        return False
    
    for i in range(2,int(n**0.5)+1):
        if n%i==0:
            return False

    return True
#%%
def hcfnaive(a,b): 
    if(b==0): 
        return a 
    else: 
        return hcfnaive(b,a%b) 


#%%
if __name__ == "__main__":
    argv = sys.argv
    if argv[1] == 'init':
        key_generator(int(argv[2]))
    elif argv[1] == '-e':
        encypher(argv[2],int(argv[3]),int(argv[4]))
    elif argv[1] == '-d':
        decypher(argv[2],int(argv[3]),int(argv[4]))
    else:
        print ('no such arg!')
#%%



# %%


# %%


# %%


