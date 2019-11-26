#%%
from PIL import Image
from Crypto.Cipher import AES
ppmPicture = 'myppm.ppm'
im = Image.open('./r1.jpg')
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
        i = int(0)
        while data:
            i += 1
            if len(data) < 16:
                pd = 16 - len(data)
                for i in range (pd):
                    data += bytes([0])
            cipher = cipher_block.encrypt(data)
            if i > (12150 + 121500)/2:
                output.write(cipher)
            else:
                output.write(data)
            data = f.read(16)
        
    finally:
        f.close()
        output.close()
# %%
def CBC_mode(key,iv):  
    try:
        f = open('myppm.ppm','rb')
        output = open('CBC_encrypt.ppm','wb')
        cipher_block = AES.new(key,AES.MODE_CBC)
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
                tmp = tmp.append(d^i)
                
            print (tmp)
            data = bytes(tmp)
            cipher = cipher_block.encrypt(data)
            output.write(cipher)
            iv = cipher
            data = f.read(16)

    finally:
        f.close()
        output.close()

# %%
