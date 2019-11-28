#%%
from PIL import Image
from Crypto.Cipher import AES
ppmPicture = 'myppm.ppm'
im = Image.open('./photo.png')
im.save(ppmPicture)
#%%
def EBC_mode(key):  
    try:
        f = open('myppm.ppm','rb')
        output = open('EBC_encrypt.ppm','wb')
        cipher_block = AES.new(key,AES.MODE_ECB)
        for i in range(3):
            data = f.readline()
            output.write(data)
            print(data)
        data = f.read(16)

        while data:
 
            if len(data) < 16:
                pd = 16 - len(data)
                for i in range (pd):
                    data += bytes([0])
            cipher = cipher_block.encrypt(data)
            output.write(cipher)

            data = f.read(16)
        
    finally:
        f.close()
        output.close()
# %%
def CBC_mode(key,iv):  
    try:
        f = open('myppm.ppm','rb')
        output = open('CBC_encrypt.ppm','wb')
        cipher_block = AES.new(key,AES.MODE_ECB)
        for i in range(3):
            data = f.readline()
            output.write(data)
            print(data)
        data = f.read(16)
        while data:
            if len(data) < 16:
                pd = 16 - len(data)
                for i in range (pd):
                    data += bytes([0])
            tmp = []
            for d,i in zip(data,iv):
                tmp.append((d ^ i) % 255)
                
            data = bytes(tmp)
            cipher = cipher_block.encrypt(data)
            output.write(cipher)
            iv = cipher
            data = f.read(16)

    finally:
        f.close()
        output.close()
#%%
def Cool_mode(key,iv):  
    try:
        f = open('myppm.ppm','rb')
        output = open('Cool_encrypt.ppm','wb')
        cipher_block = AES.new(key,AES.MODE_ECB)
        for i in range(3):
            data = f.readline()
            output.write(data)
            print(data)
        data = f.read(16)
        while data:
            if len(data) < 16:
                pd = 16 - len(data)
                for i in range (pd):
                    data += bytes([0])
            tmp = []
            for d,i in zip(data,iv):
                tmp.append((d ^ i) % 255)
                
            
            data = bytes(tmp)
            
            cipher = cipher_block.encrypt(data)
            output.write(cipher)
            
            tmp = iv[15:16]
            tmp += iv[:15]
            iv = bytes(tmp)
            data = f.read(16)

    finally:
        f.close()
        output.close()
# %%
EBC_mode(b'1234567887654321')
CBC_mode(b'1234567887654321',b'11111111ffffffff')
Cool_mode(b'1234567887654321',b'11111111ffffffff')
# %%
