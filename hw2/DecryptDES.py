import numpy as np
import sys

key = str(bin(int(sys.argv[1][2:],16)))[2:].zfill(56)
key = np.asarray(list(map(int,key)))
print (key,key.shape)
cipyphertext = str(bin(int(sys.argv[2][2:],16)))[2:].zfill(64)
cipyphertext = np.asarray(list(map(int,cipyphertext)))
print(cipyphertext,cipyphertext.shape)

