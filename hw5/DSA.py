#%%
import sys
from hashlib import sha1
import random

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
def gen_prime(len):
    prime = ''
    for i in range(len):
        if i == len - 1 or i == 0:
            prime += '1'
        else:
            prime += random.choice(['0','1'])


    while isprime(prime) == False:
        prime = ''
        for i in range(len):
            if i == len - 1 or i == 0:
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

#%%
def SAM(base, exponent, n):
    br = bin (exponent)[2:].zfill(exponent.bit_length())
    y = 1
    for k in range(0,len(br)):
        y = (y * y) % n 
        if(br[k] == '1'):
            y = (y * base) % n
    return y
#%%   
def gen_p():
    q = gen_prime(160)
    k = random.getrandbits(1024 - 160)
    count = 0
    while(1):
        count += 1
        if(count > 10000):
            q = gen_prime(160)
        p = k * q + 1
        p = bin(p)
        if isprime(p) == True and int(p,2).bit_length() == 1024:
            break
        k = random.getrandbits(1024 - 160 )
        
    p = int(p,2)
    return p,q,k
        
# %%
msg = sys.argv[1]

print ("key generate...")
p,q, k = gen_p()
print ('p = ', p ,'\n','q = ', q ,'\n','k = ',k)
h = random.randint(1,p-1)
print ('h = ', h)
g = SAM(h,k,p)
print('g = ',g)
x = random.randint(1,q-1)
print ('private key x = ',x)
y = SAM(g,x,p)
print ('private key y = ',y)
# %%
print ('message:', msg)
print ('signing...')
k = random.randint(1,q)
kinv = modinv(k,q)
SHA = sha1(msg.encode('utf-8')).hexdigest()
s = []
r = SAM(g,k,p)
r = r % q
for c in SHA:
    tmp = ((ord(c) + x * r) * kinv) % q
    s.append(tmp)
print ('sign complete')
print ('k = ', k)
print ('r = ', r)
print ('s = ', s)


# %%
print ('validtion...')
v = []
for i in range(len(s)):
    w = modinv(s[i], q)
    u1 = (w * ord(SHA[i])) % q
    u2 = (w * r) % q
    a = (SAM(g, u1, p) * SAM(y, u2, p))%p % q
    v.append(a)
print('validation info')
print('v:',v) 
flag = False
for _v in v:
    if (_v % q != r):
        flag = True
        print('validation error')
if (not flag):
    print('validation pass')   

# %%
